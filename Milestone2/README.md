## **Agentic AI for Maritime Freight Pricing and Route Optimization**

## **Milestone 2: Full-Stack AI/ML Integration & Advanced Security Engine**

This is my Milestone 2 submission. Milestone 1 delivered the standalone User Authentication module — JWT session handling, a Streamlit UI, SQLite-backed credentials, and Gmail-based OTP verification. Milestone 2 takes that security gateway and unifies it with the full product: three autonomous ML agents, a generative LLM Copilot, and a fully functional Admin Dashboard with Add / Delete / Unlock user lifecycle controls — plus three new hardening layers the security module didn't have before: progressive account lockout, a dynamic password strength checker, and Gmail OTP resend rate limiting.

The whole thing still runs inside a single Google Colab notebook. **Streamlit** powers the UI, the app runs on a **T4 GPU** runtime so the LLM Copilot can load, and **ngrok** exposes it through a public HTTPS URL so it can be opened and tested in an actual browser instead of staying locked inside Colab.

## **What Milestone 2 Adds on Top of Milestone 1**

|**Area**|**Milestone 1**|**Milestone 2**|
|---|---|---|
|**Auth**|Login, signup, JWT sessions, security-question reset|Adds progressive account lockout (3rd/4th/5th failed attempt), Gmail OTP resend cooldown ladder|
|**Password Policy**|Static rule enforced at signup only|Live 🔴 Weak / 🟡 Average / 🟢 Good strength badge on Register and Reset tabs, hard block under 5 characters|
|**Intelligence**|None — auth only|3 autonomous ML agents (Pricing, Route Delay, Carrier Compliance), each trained on 2 Kaggle datasets and comparing 5+ algorithms|
|**Copilot**|None|HuggingFace **Qwen2.5-3B-Instruct** (4-bit) LLM Copilot that synthesizes all 3 agents' outputs into an executive shipping strategy plus a structured JSON audit action|
|**Admin Panel**|Hidden / not functional|Fully enabled behind `role = 'Admin'` — Add User, Delete User, Unlock Account, and an ML Model Card tab|

## **Features**

|**Feature**|**What it does**|
|---|---|
|**Login**|Validates credentials against SQLite and enforces progressive lockout on repeated failures|
|**Progressive Lockout**|3rd failed attempt → 5-min lock, 4th → 15-min lock, 5th → permanent lock that only an Admin can clear|
|**OTP Resend Cooldown**|Gmail OTP resend attempts are throttled: 60s → 3 min → 5 min → 1 hour on the 4th+ attempt|
|**Password Strength Checker**|Live badge as the user types: under 5 characters is blocked, 5–9 is Average, 10+ is Good|
|**Agent 1 — Dynamic Pricing**|Regression on SCMS Delivery History + DataCo Smart Supply Chain data, compares 5+ algorithms, champion picked by R² (target ≥ 0.90)|
|**Agent 2 — Route Delay Classifier**|Classification on Supply Chain Analysis + International Trade Logistics data, compares 5+ algorithms, champion picked by ROC-AUC|
|**Agent 3 — Carrier Compliance Sentinel**|Classification on Freight Carrier Performance + Logistics Shipment Audit data, compares 5+ algorithms, champion picked by ROC-AUC|
|**AI Copilot**|Qwen2.5-3B (4-bit) chat that reasons over the 3 agents' live outputs and returns a structured JSON audit action; falls back to a rule-based response if no GPU is attached|
|**Admin Dashboard**|Add User form, Delete User button, Unlock Account button, and an ML Model Card tab showing each agent's saved metrics|

## **System Architecture**

|**Phase**|**Module**|**Responsibility**|
|---|---|---|
|**Phase 1 — Security Gateway**|`auth.py`, `db.py`|Enforces Login, Registration, and Forgot Password (Gmail OTP) before unlocking the UI. Stores hashed credentials and progressive lockout state in SQLite (`users` table).|
|**Phase 2 — Domain Intelligence**|`train_ml_freight.py`|Once authenticated, unlocks Agent 1: Dynamic Pricing, Agent 2: Route Delay Classifier, and Agent 3: Carrier Compliance Sentinel tabs.|
|**Phase 3 — Generative Advisory**|`llm_engine_freight.py`|Integrates HuggingFace LLM orchestration to synthesize the 3 agents' numerical outputs into an executive shipping strategy and a structured JSON audit action.|
|**Phase 4 — System Administration**|`admin_dash.py`|Dedicated administrative controls restricted exclusively to users authenticated with `role = 'Admin'`.|

## **Indian Port Coverage**

|**Port**|**Location**|
|---|---|
|**JNPT**|Mumbai, Maharashtra|
|**Mundra**|Gujarat|
|**Chennai**|Tamil Nadu|
|**Cochin**|Kerala|

## **Progressive Account Lockout**

|**Failed Attempts**|**Action**|**User-Facing Message**|
|---|---|---|
|3rd consecutive|`lock_until = now() + 5 min`|⏳ Account temporarily locked for 5 minutes due to 3 failed attempts.|
|4th consecutive|`lock_until = now() + 15 min`|⏳ Account temporarily locked for 15 minutes due to 4 failed attempts.|
|5th consecutive|`account_status = 'locked'`|❌ Account permanently locked due to 5 failed attempts. Only the System Administrator can unlock this account via the Admin Dashboard.|

On a successful login where `now() >= lock_until`, `failed_attempts` resets to 0 and `lock_until` clears.

## **OTP Resend Cooldown**

|**Resend Attempt**|**Cooldown**|**Notification**|
|---|---|---|
|1st resend|60 seconds|⏳ Please wait 60 seconds before requesting another OTP.|
|2nd resend|180 seconds (3 min)|⏳ Please wait 3 minutes before requesting another OTP.|
|3rd resend|300 seconds (5 min)|⏳ Please wait 5 minutes before requesting another OTP.|
|4th+ resend|3,600 seconds (1 hour)|⚠️ Too many OTP requests. Please wait 1 hour before trying again.|

## **Password Strength Policy**

|**Length**|**Badge**|**Submission Behavior**|
|---|---|---|
|< 5 characters|🔴 Weak|Blocked — "Password too weak (minimum 5 characters required)."|
|5–9 characters|🟡 Average|Allowed — "🟡 Average strength (10+ characters recommended for enterprise security)."|
|10+ characters|🟢 Good|Allowed — "🟢 Good password strength — proceed with bcrypt hashing."|

## **ML Agents & Datasets**

|**Agent**|**Metric**|**Kaggle Datasets**|**Algorithms Compared**|
|---|---|---|---|
|**Agent 1 — Dynamic Pricing** (Regression)|R² ≥ 0.90|SCMS Delivery History, DataCo Smart Supply Chain|RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor, Ridge Regression, + 2 more (Decision Tree / AdaBoost / KNN)|
|**Agent 2 — Route Delay Classifier**|ROC-AUC optimized|Supply Chain Analysis Data, International Trade Logistics|RandomForestClassifier, GradientBoostingClassifier, LogisticRegression, SVC (RBF), + 2 more (Extra Trees / AdaBoost / KNN)|
|**Agent 3 — Carrier Compliance Sentinel**|ROC-AUC optimized|Freight Carrier Performance, Logistics Shipment Audit Data|GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier, LogisticRegression, + 2 more (Decision Tree / AdaBoost / MLP)|

Champion models are saved to `joblib` and their metrics are logged to the `ml_models` table for the Admin Panel's ML Model Card tab.

## **Tech Stack**

|**Layer**|**Tools Used**|
|---|---|
|**Frontend / UI**|Streamlit, `ui_theme.py`|
|**Backend / Auth**|PyJWT, bcrypt|
|**Database**|SQLite|
|**ML**|scikit-learn (RandomForest, GradientBoosting, ExtraTrees, AdaBoost, Ridge, Logistic Regression, Decision Tree, KNN, SVC, MLP), joblib|
|**LLM Copilot**|HuggingFace Transformers, bitsandbytes (4-bit quantization), Qwen2.5-3B-Instruct|
|**Data**|kagglehub — SCMS Delivery, DataCo Smart Supply Chain, and 4 more Kaggle logistics datasets|
|**Email / OTP**|Gmail SMTP with an App Password (console fallback if not configured)|
|**Deployment**|pyngrok (public HTTPS tunnel from Colab)|
|**Secrets**|Google Colab Secrets, propagated to `os.environ` for the Streamlit subprocess|

**Security note:** Passwords are hashed with **bcrypt** before touching the database. Sensitive values — JWT secret, ngrok token, HF token, admin credentials, and email credentials — are stored only in **Colab Secrets** and are never hard-coded in the notebook.

## **Repository Structure**

```
Infosys Repository/
└── Milestone2/
    ├── FreightQuote_AI_Milestone2.ipynb
    ├── auth.py
    ├── db.py
    ├── ui_theme.py
    ├── admin_dash.py
    ├── train_ml_freight.py
    ├── llm_engine_freight.py
    ├── requirements.txt
    ├── README.md
    └── screenshots/
```

## **How to Run**

### 1. Switch the runtime to GPU

`Runtime → Change runtime type → T4 GPU → Save`, then run `!nvidia-smi` as the first code cell to confirm the GPU is attached. The Copilot loads Qwen2.5-3B-Instruct 4-bit (`load_in_4bit=True` via bitsandbytes), which fits comfortably on a single T4.

### 2. (Recommended) Create a Kaggle API token

Log in at kaggle.com → profile picture → **Settings → API → Create New Token**. This downloads a `kaggle.json` containing a username and key. Add both as Colab Secrets below, or upload the file to `~/.kaggle/kaggle.json`. This lets the pricing/route/compliance models train on real logistics data instead of synthetic data — the notebook still works without it.

### 3. Store all secrets in Colab Secrets (never hard-code them)

Click the key icon (Secrets) in the left sidebar, add each secret below, and toggle notebook access ON for each.

|**Secret Name**|**How to Get It**|**Used For**|
|---|---|---|
|`JWT_SECRET_KEY`|Any long random string / passphrase — never transmitted, only signs tokens locally|Signs & verifies login session tokens|
|`ADMIN_EMAIL_ID`|Any email you choose — becomes the Admin Panel login (falls back to `infosys@ai`)|Bootstraps the admin account on first run|
|`ADMIN_PASSWORD`|Any password meeting the strength rule (8+ chars, upper, lower, number, symbol)|Bootstraps the admin account on first run|
|`NGROK_AUTHTOKEN`|Free account at ngrok.com → dashboard → copy Authtoken|Gives the Streamlit app a public HTTPS URL|
|`HF_TOKEN`|HuggingFace account → Settings → Access Tokens|Authenticates HuggingFace LLM Copilot inference (Qwen2.5-3B, 4-bit)|
|`EMAIL_ID`|The Gmail address OTP/alert emails are sent from|Sender address for real OTP emails (optional — console fallback works without it)|
|`EMAIL_PASSWORD`|Gmail → 2-Step Verification → App Passwords → create a 16-character app password|Authenticates the Gmail SMTP sender for OTP emails|
|`KAGGLE_USERNAME` / `KAGGLE_KEY`|From the `kaggle.json` downloaded in Step 2|Optional — trains models on real Kaggle data instead of synthetic data|

### 4. Run the cells in order

- pip install cell
- secrets + Google Drive mount cell
- GPU check + Qwen2.5-3B load cell
- `%%writefile` cells for `db.py`, `ui_theme.py`, `auth.py`, `admin_dash.py`, `train_ml_freight.py`, `llm_engine_freight.py`, and the main Streamlit app
- ML training cell (trains and compares 5+ algorithms per agent)
- launcher cell (starts Streamlit + opens the ngrok tunnel)

### 5. Open the app

The launcher cell prints a public **ngrok URL** — open it in a new browser tab.

### 6. Try it out

- Register a new account and verify it with the OTP emailed to you
- Trigger progressive lockout by entering the wrong password 3–5 times
- Test **Forgot Password** end-to-end with OTP, including the resend cooldown ladder
- Log in with the admin credentials and try Add User, Delete User, and Unlock Account
- Open the **AI Copilot** and ask it to explain a freight risk scenario, e.g. *"Explain in 2 sentences why port congestion increases freight risk."*
- Check the **ML Pricing Calculator** for a predicted cost, and the **ML Model Card** tab for R²/ROC-AUC across all 3 agents

### 7. Shut it down

Interrupt the launcher cell (Ctrl+C or the Colab stop button) to stop the Streamlit process and close the ngrok tunnel.

## **Finalizing the Notebook**

Before uploading, this project was restarted and re-run top to bottom, all cell outputs were cleared, and the notebook was searched for any hard-coded email address, JWT secret, ngrok token, Kaggle key, or admin password so that only Colab-secrets lookups remain. The final notebook was uploaded as `FreightQuote_AI_Milestone2.ipynb` inside the `Milestone2` folder of the Infosys Repository.

## **Screenshots**

Screenshots are stored in the `screenshots/` folder inside this same directory.

|**Page**|**Preview**|
|---|---|
|Home Page|screenshots/home.jpeg|
|AI Copilot (prompt + response)|screenshots/ai_copilot.jpeg|
|ML Pricing Calculator|screenshots/ml_pricing_calculator.jpeg|
|Admin Panel — ML Model Card|screenshots/ml_model_card.jpeg|
|Admin Panel — Add / Delete / Unlock User|screenshots/admin_user_lifecycle.jpeg|
|Triggered Lockout Message|screenshots/lockout_message.jpeg|
|OTP Resend Cooldown Message|screenshots/otp_cooldown.jpeg|

## **Home Page**

<img width="1600" height="757" alt="home" src="https://github.com/user-attachments/assets/75726f3b-c403-4e27-8cfa-f3886e9ee828" />

## **AI Copilot (prompt + response)**

<img width="1600" height="768" alt="ai_copilot" src="https://github.com/user-attachments/assets/166ef148-c97a-49d3-9af1-10479b3b70a7" />

## **ML Pricing Calculator**

<img width="1600" height="758" alt="ml_pricing_calculator" src="https://github.com/user-attachments/assets/142affb5-71be-47a2-a286-bff459616f44" />

## **Admin Panel — ML Model Card**

<img width="1600" height="758" alt="ml_model_card" src="https://github.com/user-attachments/assets/da5c2264-ecff-41bd-8512-08986e820958" />

## **Admin Panel — Add / Delete / Unlock User**

<img width="1600" height="758" alt="admin_user_lifecycle" src="https://github.com/user-attachments/assets/8239ac9e-6860-4669-96ef-e5065ee84b08" />

## **Triggered Lockout Message**

<img width="1446" height="792" alt="lockout_message" src="https://github.com/user-attachments/assets/acdbbb04-85f8-406a-9db9-8d9eca70978a" />

## **OTP Resend Cooldown Message**

<img width="1127" height="792" alt="otp_cooldown" src="https://github.com/user-attachments/assets/3710b330-3ac5-4086-a9e2-37e7c4505f4e" />
