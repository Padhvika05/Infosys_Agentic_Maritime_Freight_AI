# ⚡ Maritime Freight Portal — FreightQuote AI

### End-to-End AI-Powered Maritime Freight Intelligence Platform (Milestone 4)

---

## 📌 Overview

**FreightQuote AI** is an end-to-end, AI-powered maritime freight intelligence platform. It helps logistics teams get instant, grounded answers about shipments, freight pricing, carrier performance, customs, weather risk, and documentation.

The project is built across **three integrated notebooks**, each responsible for a distinct layer of the system:

| Notebook | Purpose |
|----------|---------|
| `Maritime_Freight_Portal_Milestone4.ipynb` | The main Streamlit application — UI, authentication, all 9 AI agents, admin dashboard, and deployment |
| `Copy_of_FreightQuote_Data_Pipeline_ML_Trainer.ipynb` | Data pipeline & AutoML trainer — downloads Kaggle datasets and trains ML models for each agent |
| `FreightQuote_RAG_Builder__3_.ipynb` | Knowledge base builder — crawls documents/PDFs and builds the FAISS + BM25 retrieval indexes powering the RAG-based AI Copilot |

Together, these three notebooks form a complete pipeline: **data & model training → knowledge base indexing → deployed intelligent portal.**

---

## 🏗️ System Architecture

```
                ┌─────────────────────────────────────┐
                │   1. Data Pipeline & ML Trainer      │
                │   (Kaggle datasets → trained models) │
                └───────────────────┬───────────────────┘
                                    │  ML models (joblib)
                                    ▼
┌───────────────────────┐   ┌─────────────────────────────┐
│  2. RAG Builder        │   │  3. Maritime Freight Portal  │
│  (PDF/Web crawl →      │──▶│  (Streamlit app: UI, agents, │
│  FAISS + BM25 index)   │   │  auth, admin, LLM backend)   │
└───────────────────────┘   └─────────────────────────────┘
```

---

## ✨ Key Features

### 🔐 Authentication & Access Control
- Email/username login with bcrypt password hashing and JWT-based sessions
- Gmail OTP-based password reset with built-in SMTP diagnostics
- Role-Based Access Control (Admin, Operations Manager, Freight Broker, and more)

### 🤖 AI Copilot (RAG-powered)
- Grounded Q&A over live shipment, port, and pricing data
- Intent classification with automatic routing to the correct data agent
- Backed by a hybrid **FAISS + BM25** retrieval engine built in the RAG Builder notebook

### 🚢 Freight & Port Intelligence Agents
| Agent | Capability |
|-------|-----------|
| Agent 1 | Route Intelligence — interactive port maps and route analysis |
| Agent 2 | Dynamic Freight Pricing Engine |
| Agent 3 | Carrier Performance & Capacity |
| Agent 4 | Weather-Aware Freight Risk |
| Agent 5 | Dynamic Margin Predictor |
| Agent 6 | Customs, Tariffs & Compliance |
| Agent 7 | Digital Bill of Lading & Document Management |
| Agent 8 | Real-Time Incident Alerts & Multilingual Translation Studio |
| Agent 9 | PDF SOP & Freight Document RAG Studio |

### 🧠 Data Pipeline & AutoML Trainer
- Automatically downloads and merges Kaggle datasets (logistics, pricing, weather, customs, sentiment, insurance)
- Auto-detects the correct target column and task type (classification/regression) per agent
- Trains and benchmarks a 10-model competition (Random Forest, Gradient Boosting, XGBoost, AdaBoost, Extra Trees, etc.) for each of the 7 core prediction agents:
  1. Route Intelligence — arrival probability
  2. Dynamic Pricing — freight cost
  3. Weather Disruptions — delay prediction
  4. Customs Compliance — clearance prediction
  5. Margin Optimization — margin prediction
  6. Client Support — sentiment analysis
  7. Cargo Insurance — claim prediction
- Saves best-performing models to Google Drive for use by the portal

### 📚 Knowledge Base / RAG Builder
- Crawls seed websites to automatically discover and download hosted PDFs (no hardcoded document list)
- Extracts text from PDFs/HTML and chunks it for retrieval
- Builds a **synthetic freight knowledge base** covering Incoterms, customs, cargo insurance, and shipping SOPs
- Generates FAISS vector index + BM25 keyword index for hybrid semantic + keyword search
- Powers the AI Copilot and Agent 9 (PDF SOP & Document RAG Studio) with grounded, citation-ready answers

### 📊 Analytics & Monitoring
- Anomaly & risk scanner (Isolation Forest) across shipments, ports, and quotes
- Knowledge graph visualization of ports, carriers, and documents
- Global Ocean Freight Digital Twin with Monte Carlo stress testing
- Admin Dashboard — system health, user lifecycle management, LLM activity monitor, live alert log

### 🗄️ Data & Infrastructure
- SQLite database with automated seeding (50+ global ports)
- Kaggle data ingestion pipeline with schema validation
- FastAPI microservice serving a local LLM with streaming responses
- Deployed via Cloudflare Tunnel for public access from Google Colab

---

## 🛠️ Tech Stack

`Streamlit` `FastAPI` `SQLite` `FAISS` `BM25 (rank-bm25)` `Sentence Transformers` `Hugging Face Transformers` `PyTorch` `Plotly` `Folium` `bcrypt` `PyJWT` `NLLB-200 (translation)` `scikit-learn` `XGBoost` `LangChain` `BeautifulSoup / PyMuPDF (web & PDF crawling)`

---

## 🖼️ Screenshots

> Add screenshots under each subheading below to visually document the application.

### 1. Login & Authentication

<img width="1920" height="1080" alt="Screenshot (174)" src="https://github.com/user-attachments/assets/d9a3240d-8de5-459f-a6f9-be33d1be953d" />

### 2. AI Copilot
<img width="1920" height="1080" alt="Screenshot (170)" src="https://github.com/user-attachments/assets/5976ab2a-129a-4e8b-9788-2a4258c0f300" />


### 3. Agent-1
<img width="1920" height="1080" alt="Screenshot (128)" src="https://github.com/user-attachments/assets/3ba570be-f434-42de-9262-fbfdab8968a8" />

### 4. Agent-2

<img width="1920" height="1080" alt="Screenshot (129)" src="https://github.com/user-attachments/assets/8a0cf18f-8126-4946-9dc8-59a785a484cb" />

### 5. Agent-3
<img width="1920" height="1080" alt="Screenshot (131)" src="https://github.com/user-attachments/assets/8ddde081-f60f-438e-95d2-3905e885f05f" />

### 6. Agent-4

<img width="1920" height="1080" alt="Screenshot (133)" src="https://github.com/user-attachments/assets/791bd916-3e79-4c44-996b-bf07db13e289" />

### 7. Agent-5
<img width="1920" height="1080" alt="Screenshot (135)" src="https://github.com/user-attachments/assets/f96d8b8d-b40b-4a1c-a691-b67886eb20c5" />

### 8. Agent-6
<img width="1920" height="1080" alt="Screenshot (137)" src="https://github.com/user-attachments/assets/abc43634-06b5-4a70-b170-74efa11132d5" />

### 9. Agent-7
<img width="1920" height="1080" alt="Screenshot (138)" src="https://github.com/user-attachments/assets/371687d7-d4fc-471c-99c9-c40ddac6e082" />

### 10. Agent-8

<img width="1920" height="1080" alt="Screenshot (139)" src="https://github.com/user-attachments/assets/86a2ecb4-e738-4743-a864-504245019783" />

### 11. Notification

<img width="1920" height="1080" alt="Screenshot (141)" src="https://github.com/user-attachments/assets/8b7e6696-dd89-4a62-a7ad-2d0c3d3c264f" />

### 12. Digital Twin
<img width="1920" height="1080" alt="Screenshot (145)" src="https://github.com/user-attachments/assets/086a7b4d-5411-4ab7-a63d-def2a6cc9f77" />


### 13. Admin Dashboard
<img width="1920" height="1080" alt="Screenshot (149)" src="https://github.com/user-attachments/assets/2e51aa64-4de3-4024-ba8d-9ef5aeab66a1" />


### 14. Forgot Password

<img width="1920" height="1080" alt="Screenshot (172)" src="https://github.com/user-attachments/assets/ae7a8a35-136b-4f7d-8c33-a2dbb9fbc730" />

### 15.OTP Flow

<img width="1920" height="1080" alt="Screenshot (176)" src="https://github.com/user-attachments/assets/88453edb-62f6-4a17-a000-5c30dae1017e" />








---

## 👥 Team Contributions

| Name | Contribution |
|------|--------------|
| **Alakshya Nilesh Salvi** | Authentication module (login, registration, RBAC) and Gmail OTP integration |
| **Simran Kapoor** | AI Copilot, LLM engine, and RAG pipeline (FAISS/BM25 hybrid retrieval, RAG Builder notebook) |
| **Nadendla Padhvika** | Freight & pricing agents (Route Intelligence, Dynamic Pricing, Margin Predictor) and analytics dashboards |
| **S Uday Gowda** | Admin Dashboard, database design/seeding, deployment (FastAPI backend, Cloudflare Tunnel), and Data Pipeline/ML Trainer notebook |
| **Manuru Deepika** | UI theme design, Multilingual Translation Studio, and documentation |

---

## 🔑 Default Admin Login

```
Email: admin@infosys.com
Password: admin123
```

---

## ⚙️ Setup Notes

- Requires `EMAIL_ID` and a Google App Password (as Colab Secrets) for real Gmail OTP delivery
- Run notebooks in order for a fresh setup:
  1. `Copy_of_FreightQuote_Data_Pipeline_ML_Trainer.ipynb` — trains and saves ML models to Google Drive
  2. `FreightQuote_RAG_Builder__3_.ipynb` — builds the FAISS/BM25 knowledge base
  3. `Maritime_Freight_Portal_Milestone4.ipynb` — launches the full Streamlit application
- Runs on Google Colab with GPU acceleration recommended
- Public access enabled via Cloudflare Tunnel (`cloudflared`)

---

<p align="center"><i>Built as part of the Infosys Springboard Internship Program.</i></p>
