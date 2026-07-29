# **<mark>Intelligent Freight Quote Generation System</mark>** 

# **Milestone 2: Full-Stack AI/ML Integration & Advanced Security Engine**

This is my Milestone 2 submission. Milestone 1 delivered the standalone User Authentication module — JWT session handling, a Streamlit UI, SQLite-backed credentials, and Gmail-based OTP verification. Milestone 2 takes that security gateway and unifies it with the full product: three autonomous ML agents, a generative LLM Copilot, and a fully functional Admin Dashboard with Add / Delete / Unlock user lifecycle controls — plus three new hardening layers the security module didn't have before: progressive account lockout, a dynamic password strength checker, and Gmail OTP resend rate limiting. 

The whole thing still runs inside a single Google Colab notebook. **Streamlit** powers the UI, the app runs on a **T4 GPU** runtime so the LLM Copilot can load, and **ngrok** exposes it through a public HTTPS URL so it can be opened and tested in an actual browser instead of staying locked inside Colab. 

# **What Milestone 2 Adds on Top of Milestone 1** 

**Area Milestone 1 Milestone 2** Login, signup, JWT Adds progressive account lockout (3rd/4th/5th failed attempt), **Auth** sessions, securityGmail OTP resend cooldown ladder question reset **Passw** Static rule enforced Live 🟡 🟢 Weak / Average / 🟢Good strength badge on Register and **ord** at signup only Reset tabs, hard block under 5 characters **Policy** 3 autonomous ML agents (Pricing, Route Delay, Carrier **Intelli gence**<sup>None — auth only</sup> Compliance), each trained on 2 Kaggle datasets and comparing 5+ algorithms HuggingFace **Qwen2.5-3B-Instruct** (4-bit) LLM Copilot that **Copil** None synthesizes all 3 agents' outputs into an executive shipping strategy **ot** plus a structured JSON audit action **Admi** Hidden / not Fully enabled behind `role = 'Admin'` — Add User, Delete User, **n** functional Unlock Account, and an ML Model Card tab **Panel** 

# **Features** 

|**Feature**|**What it does**|
|---|---|
|**Login**|Validates credentials against SQLite and enforces progressive lockout on<br>repeated failures|
|**Progressive**|3rd failed attempt → 5-min lock, 4th → 15-min lock, 5th → permanent lock|
|**Lockout**|that only an Admin can clear|
|**OTP Resend**|Gmail OTP resend attempts are throttled: 60s → 3 min → 5 min → 1 hour|



**Cooldown** on the 4th+ attempt **Password** Live badge as the user types: under 5 characters is blocked, 5–9 is Average, **Strength Checker** 10+ is Good **Agent 1 —** Regression on SCMS Delivery History + DataCo Smart Supply Chain data, **Dynamic Pricing** compares 5+ algorithms, champion picked by R² (target ≥ 0.90) **Agent 2 — Route** Classification on Supply Chain Analysis + International Trade Logistics **Delay Classifier** data, compares 5+ algorithms, champion picked by ROC-AUC **Agent 3 — Carrier** Classification on Freight Carrier Performance + Logistics Shipment Audit **Compliance** data, compares 5+ algorithms, champion picked by ROC-AUC **Sentinel** Qwen2.5-3B (4-bit) chat that reasons over the 3 agents' live outputs and **AI Copilot** returns a structured JSON audit action; falls back to a rule-based response if no GPU is attached **Admin** Add User form, Delete User button, Unlock Account button, and an ML **Dashboard** Model Card tab showing each agent's saved metrics 

# **System Architecture** 

**Phase Module Responsibility Phase 1 —** Enforces Login, Registration, and Forgot Password (Gmail OTP) **Security** `auth.py` , before unlocking the UI. Stores hashed credentials and progressive `db.py` **Gateway** lockout state in SQLite ( `users` table). **Phase 2 —** `train_m` Once authenticated, unlocks Agent 1: Dynamic Pricing, Agent 2: Route **Domain** `l_freig` **Intelligence** `ht.py` Delay Classifier, and Agent 3: Carrier Compliance Sentinel tabs. **Phase 3 —** `llm_eng` Integrates HuggingFace LLM orchestration to synthesize the 3 agents' **Generative** `ine_fre` numerical outputs into an executive shipping strategy and a structured **Advisory** `ight.py` JSON audit action. **Phase 4 — System** `admin_d` Dedicated administrative controls restricted exclusively to users **Administratio** `ash.py` authenticated with `role = 'Admin'` . 

**n** 

# **Indian Port Coverage** 

**Port Location** Mumbai, **JNPT** Maharashtra **Mundr** Gujarat **a Chenna** Tamil Nadu **i Cochin** Kerala 

# **Progressive Account Lockout** 

**Failed Attemp Action User-Facing Message ts** 

3rd `lock_until =` consecu `now() + 5` ⏳ Account temporarily locked for 5 minutes due to 3 failed attempts. tive `min` 4th `lock_until =` consecu `now() + 15` ⏳ Account temporarily locked for 15 minutes due to 4 failed attempts. tive `min` 5th `account_stat` 🟢 Account permanently locked due to 5 failed attempts. Only the consecu `us =` System Administrator can unlock this account via the Admin tive `'locked'` Dashboard. 

On a successful login where `now() >= lock_until` , `failed_attempts` resets to 0 and `lock_until` clears. 

# **OTP Resend Cooldown** 

**Resend Cooldown Notification Attempt** 1st resend 60 seconds ⏳ Please wait 60 seconds before requesting another OTP. 180 seconds (3 2nd resend ⏳ Please wait 3 minutes before requesting another OTP. min) 300 seconds (5 3rd resend ⏳ Please wait 5 minutes before requesting another OTP. min) 3,600 seconds (1 ⚠️� Too many OTP requests. Please wait 1 hour before trying 4th+ resend hour) again. 

# **Password Strength Policy** 

**Length Badge Submission Behavior** < 5 🟢 Weak Blocked — "Password too weak (minimum 5 characters required)." characters 5–9 🟡 Allowed — "🟡 Average strength (10+ characters recommended for characters Average enterprise security)." 10+ 🟢 Good Allowed — "🟢 Good password strength — proceed with bcrypt hashing." characters 

# **ML Agents & Datasets** 

|**Agent**|**Metri**|**c**<br>**Kaggle Datasets**|**Algorithms Compared**|
|---|---|---|---|
|**Agent 1 —**||SCMS Deliver|RandomForestRegressor,|
|**Dynamic**|R² ≥|y<br>Hitr DtC|GradientBoostingRegressor, ExtraTreesRegressor,|
|**Pricing**|0.90|soy, aao<br>Smart Sul Chain|Ridge Regression, + 2 more (Decision Tree /|
|(Regression)||ppy|AdaBoost / KNN)|



|**Agent 2 —**<br>**Route Dela**|ROC-<br>AUC|Supply Chain<br>Analysis Data,|RandomForestClassifier,<br>GradientBoostingClassifier, LogisticRegression,|
|---|---|---|---|
|**y**<br>**Classifier**|optimiz<br>ed|International Trade<br>Logistics|SVC (RBF), + 2 more (Extra Trees / AdaBoost /<br>KNN)|
|**Agent 3 —**|ROC-|Freight Carrier|GradientBoostingClassifier,|
|**Carrier**|AUC|Performance,|RandomForestClassifier, ExtraTreesClassifier,|
|**Compliance**|optimiz|Logistics Shipment|LogisticRegression, + 2 more (Decision Tree /|
|**Sentinel**|ed|Audit Data|AdaBoost / MLP)|



Champion models are saved to `joblib` and their metrics are logged to the `ml_models` table for the Admin Panel's ML Model Card tab. 

# **Tech Stack** 

**Layer Fronten** Streamlit, `ui_theme.py` **d / UI Backend** PyJWT, bcrypt **/ Auth Database** SQLite 

**Tools Used** 

scikit-learn (RandomForest, GradientBoosting, ExtraTrees, AdaBoost, Ridge, Logistic **ML** Regression, Decision Tree, KNN, SVC, MLP), joblib 

**LLM** HuggingFace Transformers, bitsandbytes (4-bit quantization), Qwen2.5-3B-Instruct **Copilot** kagglehub — SCMS Delivery, DataCo Smart Supply Chain, and 4 more Kaggle **Data** logistics datasets 

**Email /** Gmail SMTP with an App Password (console fallback if not configured) **OTP** 

**Deploym** pyngrok (public HTTPS tunnel from Colab) **ent** 

**Secrets** Google Colab Secrets, propagated to `os.environ` for the Streamlit subprocess **Security note:** Passwords are hashed with **bcrypt** before touching the database. Sensitive values — JWT secret, ngrok token, HF token, admin credentials, and email credentials — are stored only in **Colab Secrets** and are never hard-coded in the notebook. 

# **Repository Structure** 

Infosys Repository/ 

└── Milestone2/ 

├── FreightQuote_AI_Milestone2.ipynb 

├── auth.py 

├── db.py 

├── ui_theme.py ├── admin_dash.py ├── train_ml_freight.py 

├── llm_engine_freight.py 

├── requirements.txt ├── README.md └── screenshots/ 

# **How to Run** 

## **1. Switch the runtime to GPU** 

`Runtime → Change runtime type → T4 GPU → Save` , then run `!nvidia-smi` as the first code cell to confirm the GPU is attached. The Copilot loads Qwen2.5-3B-Instruct 4-bit ( `load_in_4bit=True` via bitsandbytes), which fits comfortably on a single T4. 

## **2. (Recommended) Create a Kaggle API token** 

Log in at kaggle.com → profile picture → **Settings → API → Create New Token** . This downloads a `kaggle.json` containing a username and key. Add both as Colab Secrets below, or upload the file to `~/.kaggle/kaggle.json` . This lets the pricing/route/compliance models train on real logistics data instead of synthetic data — the notebook still works without it. 

## **3. Store all secrets in Colab Secrets (never hard-code them)** 

Click the key icon (Secrets) in the left sidebar, add each secret below, and toggle notebook access ON for each. 

|**Secret Name**|**How to Get It**|**Used For**|
|---|---|---|
|`JWT_SECRET_`<br>`KEY`|Any long random string / passphrase —<br>never transmitted, only signs tokens<br>locally|Signs & verifies login session tokens|
|`ADMIN_EMAIL`<br>`_ID`|Any email you choose — becomes the<br>Admin Panel login (falls back to<br>`infosys@ai`)|Bootstraps the admin account on first<br>run|
|`ADMIN_PASSW`|Any password meeting the strength rule|Bootstraps the admin account on first|
|`ORD`|(8+ chars, upper, lower, number, symbol)|run|
|`NGROK_AUTHT`<br>`OKEN`|Free account at ngrok.com → dashboard<br>→ copy Authtoken|Gives the Streamlit app a public<br>HTTPS URL|
|`HF_TOKEN`|HuggingFace account → Settings →<br>Access Tokens|Authenticates HuggingFace LLM<br>Copilot inference (Qwen2.5-3B, 4-bit)|



The Gmail address OTP/alert emails are `EMAIL_ID` sent from 

Gmail → 2-Step Verification → App `EMAIL_PASSW ORD` Passwords → create a 16-character app password `KAGGLE_USER` From the `kaggle.json` downloaded in `NAME` / Step 2 `KAGGLE_KEY` 

Sender address for real OTP emails (optional — console fallback works without it) 

Authenticates the Gmail SMTP sender for OTP emails 

Optional — trains models on real Kaggle data instead of synthetic data 

## **4. Run the cells in order** 

- pip install cell 

- secrets + Google Drive mount cell 

- GPU check + Qwen2.5-3B load cell 

- `%%writefile` cells for `db.py` , `ui_theme.py` , `auth.py` , `admin_dash.py` , `train_ml_freight.py` , `llm_engine_freight.py` , and the main Streamlit app 

- ML training cell (trains and compares 5+ algorithms per agent) 

- launcher cell (starts Streamlit + opens the ngrok tunnel) 

## **5. Open the app** 

The launcher cell prints a public **ngrok URL** — open it in a new browser tab. 

## **6. Try it out** 

- Register a new account and verify it with the OTP emailed to you 

- Trigger progressive lockout by entering the wrong password 3–5 times 

- Test **Forgot Password** end-to-end with OTP, including the resend cooldown ladder 

- Log in with the admin credentials and try Add User, Delete User, and Unlock Account 

- Open the **AI Copilot** and ask it to explain a freight risk scenario, e.g. _"Explain in 2 sentences why port congestion increases freight risk."_ 

- Check the **ML Pricing Calculator** for a predicted cost, and the **ML Model Card** tab for R²/ROCAUC across all 3 agents 

## **7. Shut it down** 

Interrupt the launcher cell (Ctrl+C or the Colab stop button) to stop the Streamlit process and close the ngrok tunnel. 

# **Finalizing the Notebook** 

Before uploading, this project was restarted and re-run top to bottom, all cell outputs were cleared, and the notebook was searched for any hard-coded email address, JWT secret, ngrok token, Kaggle key, or admin password so that only Colab-secrets lookups remain. The final notebook was uploaded as `FreightQuote_AI_Milestone2.ipynb` inside the `Milestone2` folder of the Infosys Repository. 

# **Screenshots** 

Screenshots are stored in the `screenshots/` folder inside this same directory. 

### **Page** 

Home Page AI Copilot (prompt + response) 

ML Pricing Calculator 

Admin Panel — ML Model Card Admin Panel — Add / Delete / Unlock User Triggered Lockout Message OTP Resend Cooldown Message 

### **Preview** 

screenshots/home.jpeg screenshots/ai_copilot.jpeg screenshots/ ml_pricing_calculator.jpeg screenshots/ml_model_card.jpeg 

screenshots/admin_user_lifecycle.jpeg screenshots/lockout_message.jpeg screenshots/otp_cooldown.jpeg 

