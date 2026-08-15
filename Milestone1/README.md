## **Agentic AI for Maritime Freight Pricing and Route Optimization** 

## **Milestone 1: User Authentication Module** 

This is my Milestone 1 submission — a complete authentication system built from scratch, not just a login form. It covers login, signup, and forgot password with two recovery routes, proper session handling with JWT, field validation, and two separate dashboards — one for a regular user and one for an admin. 

The whole thing runs inside a single Google Colab notebook. **Streamlit** powers the UI, the app runs as a background process, and **ngrok** exposes it through a public URL so it can be opened and tested in an actual browser instead of staying locked inside Colab. 

## **Features** 

| **Feature** | **What it does** |
|---|---|
| **Login** | Validates email + password, shows one generic error on failure — never reveals which field was wrong |
| **Signup** | Collects username, email, password, confirm password, security question & answer — enforces uniqueness on username/email |
| **Forgot Password** | Two recovery routes on one page — Security Question **or** OTP-by-email |
| **Field Validation** | Email format check (ab@cd.ef shape) + strict password rule (8+ chars, upper, lower, number, special symbol) |
| **JWT Sessions** | Token issued on login, verified before showing the dashboard, auto-expires after 2 hours |
| **User Dashboard** | Welcome banner, sample analytics cards, and a live system health gauge |
| **Admin Dashboard** | Separate hard-coded admin login (not a signup account) — lists every registered user's username & email, **never** passwords |
| **OTP Emails** | Sent via Gmail SMTP with an App Password, styled as a branded HTML email instead of plain text |
| **Custom UI Theme** | Consistent color palette and neo-brutalist styling applied across every page |

## **Tech Stack** 

| **Layer** | **Tools Used** |
|---|---|
| **Frontend / UI** | Streamlit, streamlit-option-menu, Plotly |
| **Backend / Auth** | PyJWT, bcrypt |
| **Database** | SQLite |
| **Email / OTP** | smtplib, email.mime, email-validator |
| **Deployment** | pyngrok (public tunnel from Colab) |
| **Secrets** | Google Colab Secrets (userdata) |

**Security note:** Passwords and security answers are hashed with **bcrypt** before ever touching the database. Sensitive values — JWT secret, ngrok token, email credentials — are stored in **Colab Secrets**, never hard-coded in the notebook. 

## **How to Run** 

## **1. Set up your secrets** 

Open the notebook in Google Colab → click the **key icon** in the left sidebar → add these four secrets and toggle **notebook access ON** for each: 

| **Secret Name** | **Value** |
|---|---|
| JWT_SECRET | Any long random string |
| NGROK_AUTHTOKEN | Copied from your ngrok dashboard |
| EMAIL_ADDRESS | Gmail address that sends the OTPs |
| EMAIL_PASSWORD | A Gmail **App Password** (needs 2-Step Verification turned on first) |

## **2. Run the cells in order** 

- pip install cell 
- imports + secrets cell 
- database + helper functions cell 
- JWT + session management cell 
- %%writefile app.py cell 
- launcher cell (starts Streamlit + opens ngrok tunnel) 

## **3. Open the app** 

The last cell prints a public **ngrok URL** — open it in a new browser tab. 

## **4. Try it out** 

- Sign up a new account 
- Log in and check out the dashboard 
- Test **Forgot Password** with both the security question and OTP routes 
- Log in with the admin credentials to see the admin dashboard 

## **5. Shut it down** 

Interrupt the last cell (Ctrl+C or the Colab stop button) — it cleans up the ngrok tunnel and kills the Streamlit process automatically. 

## **Screenshots** 

Screenshots are stored in the screenshots/ folder inside this same directory. 

| **Page** | **Preview** |
|---|---|
| Login | screenshots/login.jpeg |
| Signup | screenshots/signup.jpeg |
| Forgot Password — Security Question | screenshots/forgot_security_question.jpeg |
| Forgot Password — OTP | screenshots/forgot_otp.jpeg |
| OTP Email Received | screenshots/otp_email.jpeg |
| User Dashboard | screenshots/user_dashboard.jpeg |
| Admin Dashboard | screenshots/admin_dashboard.jpeg |
| Forgot Password | screenshots/forgot_password.jpeg |

## Login Page

![alt text](login.jpeg)

## Signup Page

![alt text](signup.jpeg)

## Forgot Password — Security Question Page

![alt text](forgot_security_question.jpeg)

## Forgot Password — OTP Page

![alt text](forgot_otp.jpeg)

## OTP Email Received Page

![alt text](otp_email.jpeg)

## User Dashboard Page

![alt text](user_dashboard.jpeg)

## Admin Dashboard Page

![alt text](admin_dashboard.jpeg)

## Forgot Password Page

![alt text](forgot_password.jpeg)
