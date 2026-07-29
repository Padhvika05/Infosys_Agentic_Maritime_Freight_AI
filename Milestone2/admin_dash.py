"""admin_dash.py — Shared Admin Dashboard renderer for FreightQuote & FranchiseOps AI

Milestone 2 additions (Instructions §9):
  - Add User portal (custom username / email / password / role).
  - Delete User (unchanged, now inside the lifecycle table).
  - Lock / Unlock Account buttons: Admin can manually lock any active account, or
    unlock any user with account_status='locked' or failed_attempts>=3.
  - Dedicated "ML Model Card" tab showing R²/RMSE (Pricing) and ROC-AUC (Route Delay, Carrier Audit).
"""
import subprocess, datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_conn
from notifications import get_recent_alerts
from ui_theme import render_card, COLORS, password_strength
from auth import hash_txt

_APP_START = datetime.datetime.now()


def _smi(query):
    try:
        r = subprocess.run(
            ["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=3)
        return r.stdout.strip()
    except Exception:
        return "N/A"


def render_admin_dashboard(project="freight"):
    render_card('<h3 style="margin:0;">🛡️ Admin Dashboard — System Intelligence</h3>')

    # ── 1. System Health ─────────────────────────────────────────────────────
    st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:16px 0 8px;">⚙️ System Health</h4>',
                unsafe_allow_html=True)
    gpu_mem  = _smi("memory.used")
    gpu_tot  = _smi("memory.total")
    gpu_util = _smi("utilization.gpu")
    uptime   = str(datetime.datetime.now() - _APP_START).split(".")[0]
    h1, h2, h3, h4 = st.columns(4)
    for col, icon, label, val in [
        (h1, "🖥️", "GPU VRAM Used",  f"{gpu_mem} / {gpu_tot} MB"),
        (h2, "⚡", "GPU Utilization", f"{gpu_util}%"),
        (h3, "🕒", "App Uptime",      uptime),
        (h4, "✅", "LLM Status",      "Active" if gpu_mem != "N/A" else "Standby"),
    ]:
        col.markdown(
            f'<div class="pn-card" style="text-align:center;padding:14px;">'
            f'<div style="font-size:26px;">{icon}</div>'
            f'<h3 style="margin:6px 0 2px;font-size:1.1rem;">{val}</h3>'
            f'<p style="margin:0;color:{COLORS["text_muted"]};font-size:12px;">{label}</p>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── 2. User Lifecycle Management (Add / Delete / Unlock) ────────────────
    st.markdown(f'<h4 style="color:{COLORS["text_heading"]};margin:0 0 8px;">👥 User Lifecycle Management</h4>',
                unsafe_allow_html=True)

    with st.expander("➕ Add User", expanded=False):
        with st.form("add_user_form", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            with fc1:
                nu_user = st.text_input("Username")
                nu_email = st.text_input("Email")
            with fc2:
                nu_pw = st.text_input("Initial Password", type="password")
                nu_role = st.selectbox("Role", ["Admin", "Logistics Manager", "Pricing Analyst",
                                                 "Carrier Auditor", "Executive"])
            submitted = st.form_submit_button("✨ Create Account")
            if submitted:
                if not (nu_user and nu_email and nu_pw):
                    st.warning("Please fill out all fields.")
                else:
                    _, _, blocked = password_strength(nu_pw)
                    if blocked:
                        st.warning("Password too weak (minimum 5 characters required).")
                    else:
                        try:
                            with get_conn() as conn:
                                conn.execute(
                                    "INSERT INTO users (username, email, password_hash, role, account_status) "
                                    "VALUES (?, ?, ?, ?, 'active')",
                                    (nu_user, nu_email, hash_txt(nu_pw), nu_role))
                                conn.commit()
                            st.success(f"✅ User '{nu_user}' created with role [{nu_role}].")
                            st.rerun()
                        except Exception:
                            st.error("Could not create user — email or username may already exist.")

    with get_conn() as conn:
        try:
            users_df = pd.read_sql(
                "SELECT id, username, role, email, failed_attempts, lock_until, "
                "account_status, created_at FROM users ORDER BY id DESC", conn)
        except Exception:
            users_df = pd.DataFrame(columns=["id", "username", "role", "email",
                                              "failed_attempts", "lock_until",
                                              "account_status", "created_at"])

    if users_df.empty:
        st.info("No users registered yet.")
    else:
        hh1, hh2, hh3, hh4, hh5 = st.columns([2, 1.6, 2, 1.4, 1.4])
        hh1.markdown("**User**"); hh2.markdown("**Role**"); hh3.markdown("**Status**")
        hh4.markdown("**Lock / Unlock**"); hh5.markdown("**Delete**")
        for _, row in users_df.iterrows():
            uc1, uc2, uc3, uc4, uc5 = st.columns([2, 1.6, 2, 1.4, 1.4])
            uc1.markdown(f"**{row['username']}**<br><span style='color:{COLORS['text_muted']};font-size:12px;'>{row['email']}</span>",
                         unsafe_allow_html=True)
            uc2.markdown(f'<span style="color:{COLORS["accent"]};font-weight:600;">[{row["role"]}]</span>',
                         unsafe_allow_html=True)

            is_locked = (row["account_status"] == "locked") or (row["failed_attempts"] or 0) >= 3
            if row["account_status"] == "locked":
                status_html = f'<span class="pn-badge" style="background:{COLORS["red"]};color:#fff;border-color:{COLORS["red"]};">🔒 Locked</span>'
            elif (row["failed_attempts"] or 0) >= 3:
                status_html = f'<span class="pn-badge" style="background:{COLORS["yellow"]};color:#fff;border-color:{COLORS["yellow"]};">⏳ Cooling Down</span>'
            else:
                status_html = f'<span class="pn-badge" style="background:{COLORS["green"]};color:#fff;border-color:{COLORS["green"]};">✅ Active</span>'
            uc3.markdown(status_html, unsafe_allow_html=True)

            with uc4:
                if is_locked:
                    if st.button("🔓 Unlock", key=f"unlock_user_{row['id']}", help=f"Unlock {row['username']}"):
                        with get_conn() as c:
                            c.execute("UPDATE users SET failed_attempts=0, lock_until=NULL, "
                                      "account_status='active' WHERE id=?", (row["id"],))
                            c.commit()
                        st.success("✅ User account unlocked successfully.")
                        st.rerun()
                else:
                    if st.button("🔒 Lock", key=f"lock_user_{row['id']}", help=f"Manually lock {row['username']}"):
                        with get_conn() as c:
                            c.execute("UPDATE users SET account_status='locked', lock_until=NULL "
                                      "WHERE id=?", (row["id"],))
                            c.commit()
                        st.success(f"🔒 {row['username']}'s account has been locked by the administrator.")
                        st.rerun()
            with uc5:
                if st.button("🗑️", key=f"del_user_{row['id']}", help=f"Delete {row['username']}"):
                    with get_conn() as c:
                        c.execute("DELETE FROM users WHERE id=?", (row["id"],))
                        c.commit()
                    st.success(f"Deleted {row['username']}")
                    st.rerun()

    st.markdown("---")

    # ── 3. ML Model Card + LLM Activity + Alerts ─────────────────────────────
    tab_ml, tab_llm, tab_alerts = st.tabs(["📈 ML Model Card", "🤖 LLM Activity Monitor", "🔔 Live Alert Log"])

    with tab_ml:
        st.markdown(f'<p style="color:{COLORS["text_muted"]};font-size:13px;margin:0 0 10px;">'
                    f'Champion + comparison metrics for all 3 agents — R²/RMSE for Pricing, '
                    f'ROC-AUC/Accuracy for Route Delay & Carrier Compliance.</p>', unsafe_allow_html=True)
        with get_conn() as conn:
            try:
                ml_df = pd.read_sql(
                    "SELECT agent_name AS Agent, model_name AS Algorithm, "
                    "ROUND(r2_score,4) AS 'R2 / ROC-AUC', ROUND(rmse,2) AS RMSE, "
                    "ROUND(accuracy,4) AS Accuracy, training_rows AS Rows, "
                    "created_at AS 'Trained At' FROM ml_models ORDER BY id DESC", conn)
            except Exception:
                ml_df = pd.DataFrame()
        if ml_df.empty:
            st.info("No model training records found. Run Step 6 (Train ML Agents) in the notebook.")
        else:
            mc1, mc2, mc3 = st.columns(3)
            for col, agent_key, label in [
                (mc1, "Agent1", "💰 Agent 1 · Pricing (best R²)"),
                (mc2, "Agent2", "🚢 Agent 2 · Route Delay (best ROC-AUC)"),
                (mc3, "Agent3", "✅ Agent 3 · Carrier Audit (best ROC-AUC)"),
            ]:
                sub = ml_df[ml_df["Agent"].str.contains(agent_key, na=False)]
                if not sub.empty:
                    best = sub.loc[sub["R2 / ROC-AUC"].astype(float).idxmax()]
                    col.markdown(
                        f'<div class="pn-card" style="text-align:center;padding:14px;">'
                        f'<p style="margin:0;color:{COLORS["text_muted"]};font-size:12px;">{label}</p>'
                        f'<h3 style="margin:6px 0 2px;">{best["Algorithm"]}</h3>'
                        f'<span class="agent-badge">{best["R2 / ROC-AUC"]}</span>'
                        f'</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(ml_df, use_container_width=True, hide_index=True)

    with tab_llm:
        with get_conn() as conn:
            try:
                chat_df = pd.read_sql(
                    "SELECT username, count(*) as queries FROM chat_history "
                    "WHERE role='user' GROUP BY username ORDER BY queries DESC", conn)
                total_q = int(chat_df["queries"].sum()) if not chat_df.empty else 0
            except Exception:
                chat_df = pd.DataFrame(columns=["username", "queries"])
                total_q = 0

        mc1, mc2 = st.columns([1, 1.6])
        with mc1:
            st.metric("Total Copilot Queries", total_q)
            st.dataframe(chat_df, use_container_width=True, hide_index=True)
        with mc2:
            if not chat_df.empty:
                fig = px.pie(chat_df, names="username", values="queries",
                             title="Queries per User", hole=0.4,
                             color_discrete_sequence=px.colors.sequential.Teal)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                  height=250, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)

    with tab_alerts:
        filt = st.selectbox("Filter by type", ["All", "In-App", "Email", "SMS"], key="admin_alert_filt")
        alerts = get_recent_alerts(50)
        for a in alerts:
            if filt != "All" and a[1].lower() != filt.lower():
                continue
            badge = {"email": COLORS["yellow"], "sms": COLORS["red"], "in-app": COLORS["green"]}.get(a[1].lower(), COLORS["cyan"])
            st.markdown(
                f'<div style="border-left:4px solid {badge};padding:4px 10px;margin:3px 0;'
                f'font-size:13px;"><b>[{a[1].upper()}]</b> {a[3]} '
                f'<span style="color:{COLORS["text_muted"]};float:right;">{a[4]}</span></div>',
                unsafe_allow_html=True)
