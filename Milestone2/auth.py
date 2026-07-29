"""
FreightQuote AI - auth.py
Standardized SQLite authentication system matching Login_Page (1).ipynb.
Supports Login, Register (with Enterprise Roles), Forgot Password
(via OTP OR Security Question), and JWT tokens.

Milestone 2 additions (per Instructions §5, §5.1, §6):
  - Progressive account lockout (3rd/4th/5th consecutive failed attempts).
  - Real-time password strength checker (Weak / Average / Good) on Register & Reset tabs.
  - Confirm-password validation on Register & Reset tabs.
  - Gmail-based OTP verification (with resend cooldown + 5-minute expiry) powering
    one of the two Forgot Password methods, via email_otp.py.
  - Reset Password now offers TWO methods, selectable by the user:
        1) 📧 Through Send OTP          — emailed one-time code (email_otp.py)
        2) 🛡️ Through Security Question — answer the question chosen at signup
"""
import sqlite3, jwt, bcrypt, datetime, streamlit as st
try:
    from config import DB_PATH, JWT_SECRET_KEY
    JWT_SECRET = JWT_SECRET_KEY
except (ImportError, AttributeError):
    from config import DB_PATH
    JWT_SECRET = "super-secret-freightquote-key-2026"
from ui_theme import COLORS, password_strength
from email_otp import request_otp, verify_otp, reset_resend_state, init_otp_table

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def hash_txt(t):
    return bcrypt.hashpw(t.encode(), bcrypt.gensalt()).decode()

def check_txt(t, h):
    try: return bcrypt.checkpw(t.encode(), h.encode()) if h else False
    except: return False

def make_jwt(email, username):
    return jwt.encode({"email": email, "username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)}, JWT_SECRET, algorithm="HS256")

def verify_jwt(token):
    try: return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except: return None

@st.cache_resource
def init_auth():
    init_otp_table()
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            security_question TEXT,
            security_answer_hash TEXT,
            role TEXT DEFAULT 'User',
            failed_attempts INTEGER DEFAULT 0,
            lock_until TIMESTAMP DEFAULT NULL,
            account_status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        for col, ddl in [
            ("security_question",  "ALTER TABLE users ADD COLUMN security_question TEXT"),
            ("security_answer_hash","ALTER TABLE users ADD COLUMN security_answer_hash TEXT"),
            ("failed_attempts",    "ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0"),
            ("lock_until",         "ALTER TABLE users ADD COLUMN lock_until TIMESTAMP DEFAULT NULL"),
            ("account_status",     "ALTER TABLE users ADD COLUMN account_status TEXT DEFAULT 'active'"),
        ]:
            try: conn.execute(ddl)
            except Exception: pass
        # Bootstrap the default Administrator account — role MUST be 'Admin' so
        # the Admin Dashboard (Phase 4, §9) unlocks in the sidebar.
        if not conn.execute("SELECT id FROM users WHERE email='infosys@ai'").fetchone():
            conn.execute("""INSERT OR IGNORE INTO users
                         (username, email, password_hash, security_question, security_answer_hash, role, account_status)
                         VALUES (?, ?, ?, ?, ?, ?, 'active')""",
                         ("Administrator", "infosys@ai", hash_txt("admin@123"), "What is your pet name?", hash_txt("admin"), "Admin"))
            conn.commit()
        else:
            # Make sure a pre-existing seed row is actually flagged Admin.
            conn.execute("UPDATE users SET role='Admin' WHERE email='infosys@ai' AND role!='Admin'")
            conn.commit()


# ── Progressive Account Lockout (Milestone 2 Instructions §5) ──────────────────
LOCKOUT_RULES = {
    3: (300,  "⏳ Account temporarily locked for 5 minutes due to 3 failed attempts."),
    4: (900,  "⏳ Account temporarily locked for 15 minutes due to 4 failed attempts."),
}

def _now():
    return datetime.datetime.utcnow()

def _parse_ts(ts):
    if not ts:
        return None
    try:
        return datetime.datetime.fromisoformat(ts)
    except Exception:
        try:
            return datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            return None

def _get_lock_state(conn, user_id):
    row = conn.execute(
        "SELECT failed_attempts, lock_until, account_status FROM users WHERE id=?",
        (user_id,)).fetchone()
    return row if row else (0, None, "active")

def _register_failed_attempt(conn, user_id):
    """Applies §5 progressive lockout rules after a failed login. Returns a warning message or None."""
    attempts, _, _ = _get_lock_state(conn, user_id)
    attempts += 1
    msg = None
    if attempts >= 5:
        conn.execute("UPDATE users SET failed_attempts=?, lock_until=NULL, account_status='locked' WHERE id=?",
                     (attempts, user_id))
        msg = ("❌ Account permanently locked due to 5 failed attempts. "
               "Only the System Administrator can unlock this account via the Admin Dashboard.")
    elif attempts in LOCKOUT_RULES:
        seconds, rule_msg = LOCKOUT_RULES[attempts]
        lock_until = (_now() + datetime.timedelta(seconds=seconds)).isoformat()
        conn.execute("UPDATE users SET failed_attempts=?, lock_until=? WHERE id=?",
                     (attempts, lock_until, user_id))
        msg = rule_msg
    else:
        conn.execute("UPDATE users SET failed_attempts=? WHERE id=?", (attempts, user_id))
    conn.commit()
    return msg

def _reset_lockout(conn, user_id):
    conn.execute("UPDATE users SET failed_attempts=0, lock_until=NULL WHERE id=? AND account_status!='locked'",
                 (user_id,))
    conn.commit()

def _currently_locked(account_status, lock_until):
    """Returns (is_locked: bool, message: str|None)."""
    if account_status == "locked":
        return True, ("❌ Account permanently locked. Only the System Administrator "
                       "can unlock this account via the Admin Dashboard.")
    lu = _parse_ts(lock_until)
    if lu and _now() < lu:
        remaining = int((lu - _now()).total_seconds())
        mins, secs = divmod(max(remaining, 0), 60)
        return True, f"⏳ Account temporarily locked. Try again in {mins}m {secs}s."
    return False, None


def _apply_new_password(email, new_pw, confirm_pw):
    """Shared validation + write for BOTH reset methods (OTP and Security Question).
    Returns (ok: bool, message: str)."""
    if not new_pw or not confirm_pw:
        return False, "Please fill out both password fields."
    if new_pw != confirm_pw:
        return False, "Passwords do not match."
    _, _, blocked = password_strength(new_pw)
    if blocked:
        return False, "Password too weak (minimum 5 characters required)."
    with get_conn() as conn:
        conn.execute("UPDATE users SET password_hash=? WHERE email=?", (hash_txt(new_pw), email))
        conn.commit()
    return True, "✅ Password reset successfully! Please sign in."


def _password_live_feedback(pw, confirm_pw):
    if pw:
        label, css_class, _ = password_strength(pw)
        extra = " (10+ characters recommended for enterprise security)" if css_class == "pw-avg" else ""
        st.markdown(f'<span class="{css_class}">{label}{extra}</span>', unsafe_allow_html=True)
        if confirm_pw and confirm_pw != pw:
            st.markdown('<span class="pw-weak">🔴 Passwords do not match</span>', unsafe_allow_html=True)
        elif confirm_pw and confirm_pw == pw:
            st.markdown('<span class="pw-good">🟢 Passwords match</span>', unsafe_allow_html=True)


def render_auth_portal():
    init_auth()
    if "token" not in st.session_state: st.session_state["token"] = None
    if "auth_tab" not in st.session_state: st.session_state["auth_tab"] = "Login"

    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem 0 1rem;">
        <div style="font-size:44px;margin-bottom:8px;">⚡</div>
        <h1 style="font-size:2rem !important;margin:0;">FreightQuote AI Portal</h1>
        <p style="color:{COLORS['text_muted']};font-size:14px;margin:4px 0 0;">Enterprise Multi-Agent Logistics & Pricing System</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        tab1, tab2, tab3 = st.tabs(["🔐 Sign In", "📝 Register Account", "🔑 Reset Password"])

        with tab1:
            login_email = st.text_input("Email / Username", key="l_email", placeholder="infosys@ai")
            login_pw = st.text_input("Password", type="password", key="l_pw", placeholder="••••••••")
            if st.button("🚀 Sign In to Portal", key="btn_login"):
                with get_conn() as conn:
                    user = conn.execute(
                        "SELECT id, username, email, password_hash, role, failed_attempts, lock_until, account_status "
                        "FROM users WHERE email=? OR username=?", (login_email, login_email)).fetchone()

                if not user:
                    st.error("Invalid email/username or password.")
                else:
                    uid, uname, uemail, phash, urole, attempts, lock_until, acc_status = user
                    is_locked, lock_msg = _currently_locked(acc_status, lock_until)
                    if is_locked:
                        st.error(lock_msg)
                    elif check_txt(login_pw, phash):
                        with get_conn() as conn:
                            _reset_lockout(conn, uid)
                        st.session_state["token"] = make_jwt(uemail, uname)
                        st.session_state["username"] = uname
                        st.session_state["role"] = urole
                        st.success(f"Welcome back, {uname} [{urole}]!")
                        st.rerun()
                    else:
                        with get_conn() as conn:
                            warn = _register_failed_attempt(conn, uid)
                        if warn:
                            st.error(warn)
                        else:
                            st.error("Invalid email/username or password.")

        with tab2:
            r_user = st.text_input("Username", key="r_u")
            r_email = st.text_input("Email Address", key="r_e")
            r_pw = st.text_input("Create Password", type="password", key="r_p")
            r_pw2 = st.text_input("Confirm Password", type="password", key="r_p2")
            if r_pw:
                label, css_class, blocked = password_strength(r_pw)
                extra = " (10+ characters recommended for enterprise security)" if css_class == "pw-avg" else ""
                st.markdown(f'<span class="{css_class}">{label}{extra}</span>', unsafe_allow_html=True)
                if r_pw2 and r_pw2 != r_pw:
                    st.markdown(f'<span class="pw-weak">🔴 Passwords do not match</span>', unsafe_allow_html=True)
                elif r_pw2 and r_pw2 == r_pw:
                    st.markdown(f'<span class="pw-good">🟢 Passwords match</span>', unsafe_allow_html=True)
            r_role = st.selectbox("Select Enterprise Role", ["Logistics Manager", "Pricing Analyst", "Carrier Auditor", "Executive"], key="r_role")
            r_q = st.selectbox("Security Question", ["What is your pet name?", "What city were you born in?", "What is your favorite school teacher's name?"], key="r_q")
            r_a = st.text_input("Security Answer", key="r_a", help="You'll need this later if you choose to reset your password via Security Question instead of OTP.")
            if st.button("✨ Create Enterprise Account", key="btn_reg"):
                if r_user and r_email and r_pw and r_pw2 and r_a:
                    if r_pw != r_pw2:
                        st.warning("Passwords do not match. Please re-enter.")
                    else:
                        _, _, blocked = password_strength(r_pw)
                        if blocked:
                            st.warning("Password too weak (minimum 5 characters required).")
                        else:
                            try:
                                with get_conn() as conn:
                                    conn.execute("INSERT INTO users (username, email, password_hash, security_question, security_answer_hash, role) VALUES (?, ?, ?, ?, ?, ?)",
                                                 (r_user, r_email, hash_txt(r_pw), r_q, hash_txt(r_a.lower().strip()), r_role))
                                    conn.commit()
                                st.success(f"Account registered with role [{r_role}]! Please switch to Sign In tab.")
                            except Exception as e:
                                st.error(f"Registration failed: Email or username may already exist.")
                else:
                    st.warning("Please fill out all fields.")

        with tab3:
            st.markdown(f'<p style="color:{COLORS["text_muted"]};font-size:13px;margin:0 0 10px;">'
                        f'Choose how you\'d like to verify it\'s you before setting a new password.</p>',
                        unsafe_allow_html=True)
            reset_method = st.radio(
                "Reset method", ["📧 Through Send OTP", "🛡️ Through Security Question"],
                key="reset_method", horizontal=True, label_visibility="collapsed")

            # ═══════════════════════════════════════════════════════════════
            # METHOD 1 — Through Send OTP (emailed one-time code)
            # ═══════════════════════════════════════════════════════════════
            if reset_method == "📧 Through Send OTP":
                f_email = st.text_input("Registered Email", key="f_e")

                oc1, oc2 = st.columns([1, 1])
                with oc1:
                    send_clicked = st.button("\U0001F4E7 Send OTP", key="btn_send_otp")
                with oc2:
                    resend_clicked = st.button("\U0001F501 Resend OTP", key="btn_resend_otp")

                if send_clicked or resend_clicked:
                    if not f_email:
                        st.warning("Please enter your registered email.")
                    else:
                        with get_conn() as conn:
                            exists = conn.execute("SELECT id FROM users WHERE email=?", (f_email,)).fetchone()
                        if not exists:
                            st.error("Email not found.")
                        else:
                            ok, msg = request_otp(f_email, purpose="Password Reset")
                            if ok:
                                st.session_state["reset_otp_email"] = f_email
                                if msg.startswith("📧"):
                                    st.success(msg)
                                else:
                                    # Delivery fell back to console / had an SMTP issue —
                                    # surface it clearly instead of a generic success banner.
                                    st.warning(msg)
                            else:
                                st.warning(msg)

                if st.session_state.get("reset_otp_email"):
                    st.info(f"OTP sent to **{st.session_state['reset_otp_email']}** \u2014 valid for 5 minutes "
                            f"(Instructions \u00a75.1 / \u00a78 OTP time limit). If it doesn't arrive within a "
                            f"minute, check your Spam/Promotions folder, or ask your Admin to run "
                            f"`test_email_config()` from `email_otp.py` to diagnose Gmail SMTP setup.")
                    otp_try = st.text_input("Enter 6-Digit OTP", key="f_otp", max_chars=6)
                    new_pw = st.text_input("New Password", type="password", key="f_npw")
                    confirm_pw = st.text_input("Confirm New Password", type="password", key="f_npw2")
                    _password_live_feedback(new_pw, confirm_pw)

                    if st.button("\u2705 Verify OTP & Reset Password", key="btn_f2"):
                        if not otp_try or not new_pw or not confirm_pw:
                            st.warning("Please fill out the OTP and both password fields.")
                        else:
                            ok, msg = verify_otp(st.session_state["reset_otp_email"], otp_try)
                            if not ok:
                                st.error(msg)
                            else:
                                pw_ok, pw_msg = _apply_new_password(
                                    st.session_state["reset_otp_email"], new_pw, confirm_pw)
                                if pw_ok:
                                    reset_resend_state(st.session_state["reset_otp_email"])
                                    st.success(pw_msg)
                                    st.session_state["reset_otp_email"] = None
                                else:
                                    st.warning(pw_msg)

            # ═══════════════════════════════════════════════════════════════
            # METHOD 2 — Through Security Question (no email required)
            # ═══════════════════════════════════════════════════════════════
            else:
                sq_email = st.text_input("Registered Email", key="sq_e")

                if st.button("🔍 Find Security Question", key="btn_sq_find"):
                    if not sq_email:
                        st.warning("Please enter your registered email.")
                    else:
                        with get_conn() as conn:
                            row = conn.execute(
                                "SELECT security_question, security_answer_hash FROM users WHERE email=?",
                                (sq_email,)).fetchone()
                        if not row or not row[0]:
                            st.error("Email not found, or no security question is set on this account "
                                     "— use 'Through Send OTP' instead.")
                            st.session_state["sq_reset_email"] = None
                        else:
                            st.session_state["sq_reset_email"] = sq_email
                            st.session_state["sq_reset_question"] = row[0]

                if st.session_state.get("sq_reset_email") == sq_email and st.session_state.get("sq_reset_question"):
                    st.info(f"**Security Question:** {st.session_state['sq_reset_question']}")
                    sq_answer = st.text_input("Your Answer", key="sq_a")
                    new_pw = st.text_input("New Password", type="password", key="sq_npw")
                    confirm_pw = st.text_input("Confirm New Password", type="password", key="sq_npw2")
                    _password_live_feedback(new_pw, confirm_pw)

                    if st.button("\u2705 Verify Answer & Reset Password", key="btn_sq2"):
                        if not sq_answer or not new_pw or not confirm_pw:
                            st.warning("Please fill out the answer and both password fields.")
                        else:
                            with get_conn() as conn:
                                row = conn.execute(
                                    "SELECT security_answer_hash FROM users WHERE email=?",
                                    (sq_email,)).fetchone()
                            ans_hash = row[0] if row else None
                            if not check_txt(sq_answer.lower().strip(), ans_hash):
                                st.error("❌ Incorrect answer to the security question. Please try again.")
                            else:
                                pw_ok, pw_msg = _apply_new_password(sq_email, new_pw, confirm_pw)
                                if pw_ok:
                                    st.success(pw_msg)
                                    st.session_state["sq_reset_email"] = None
                                    st.session_state["sq_reset_question"] = None
                                else:
                                    st.warning(pw_msg)
