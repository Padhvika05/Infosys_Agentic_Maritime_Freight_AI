# 🚚 Intelligent Freight Quote Generation System (IFQGS)

> **Infosys Springboard Internship 7.0 – AI Internship Project**  
> **Domain:** Artificial Intelligence | Machine Learning | Large Language Models | Retrieval-Augmented Generation (RAG)

---

# 📖 Project Overview

The **Intelligent Freight Quote Generation System (IFQGS)** is an AI-powered logistics assistant designed to simplify freight quotation, shipment analysis, and logistics decision-making through the integration of **Machine Learning**, **Large Language Models (LLMs)**, and **Retrieval-Augmented Generation (RAG)**.

The project was developed in **three progressive milestones**. The first milestone focuses on secure user authentication, the second milestone introduces AI-powered freight analysis using machine learning models and an intelligent LLM assistant, and the third milestone integrates a **RAG pipeline** that enables the system to answer logistics-related queries using information retrieved from a custom knowledge base instead of relying solely on the language model.

The system is deployed using **Google Colab**, **Streamlit**, and **Ngrok**, allowing users to securely access the application through a web browser without requiring local installation.

# ✅ Milestone 1 Features

### 🔐 Secure User Authentication
Provides a complete Login, Signup, Forgot Password, and Logout system with secure session management using JWT tokens.

### 📧 Email OTP Verification
Verifies user identity by sending a One-Time Password (OTP) through Gmail SMTP during registration and password reset.

### 🔑 JWT Authentication
Uses JSON Web Tokens to securely manage authenticated sessions and protect user access.

### 🔒 Password Encryption
Stores passwords securely using BCrypt hashing instead of plain text.

### ❓ Security Questions
Allows users to reset passwords using predefined security questions as an additional authentication layer.

### 💾 SQLite Database
Stores user information, credentials, and authentication data locally using SQLite.

### 🌐 Streamlit Web Interface
Provides a clean and responsive user interface accessible directly from the browser.

### 🌍 Public Deployment using Ngrok
Exposes the Streamlit application running on Google Colab to the internet using Ngrok.

---

# ✅ Milestone 2 Features

### 🤖 AI Freight Quote Copilot
Integrates the Qwen2.5-3B-Instruct Large Language Model to assist users with logistics-related questions and freight quote generation.

### 📊 Machine Learning Price Prediction
Predicts freight pricing using multiple regression algorithms trained on logistics datasets.

### 🚛 Route Delay Prediction
Uses classification algorithms to estimate shipment delays and transportation risks.

### ✅ Carrier Compliance Analysis
Evaluates carrier reliability and compliance using machine learning models trained on logistics data.

### 📈 Multi-Model Comparison
Compares multiple machine learning algorithms and automatically selects the best-performing model based on evaluation metrics.

### 🔐 Advanced Security Engine
Implements progressive account lockout, OTP resend cooldown, password strength validation, and enhanced authentication.

### 👨‍💼 Administrator Dashboard
Allows administrators to manage users, unlock accounts, and monitor authentication activities.

### ⚡ Optimized LLM Loading
Uses 4-bit quantization and GPU acceleration to reduce memory usage and improve inference speed.

---

# ✅ Milestone 3 (RAG) Features

### 📚 Retrieval-Augmented Generation (RAG)
Enhances the LLM by retrieving relevant information from a custom logistics knowledge base before generating responses.

### 📄 PDF Knowledge Base
Indexes logistics manuals, freight documents, shipping guidelines, and company documents for intelligent retrieval.

### 🔎 Semantic Search
Uses sentence embeddings and vector similarity search to identify the most relevant document chunks.

### 🧠 Context-Aware Response Generation
Combines retrieved document context with the LLM to produce accurate, grounded, and relevant answers.

### 📦 FAISS Vector Database
Stores vector embeddings for efficient similarity search across large document collections.

### 📑 Automatic Document Chunking
Splits large PDF documents into smaller text chunks to improve retrieval accuracy.

### 💬 Intelligent Logistics Assistant
Answers logistics-related queries using both retrieved knowledge and the reasoning capabilities of the LLM.

### 🎯 Reduced Hallucinations
Minimizes incorrect or fabricated responses by grounding answers in trusted documents.

---

# 💻 Technologies Used

| Category | Technologies |
|----------|--------------|
| Programming Language | Python 3 |
| Frontend | Streamlit |
| Backend | Python |
| Authentication | JWT, BCrypt |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| Deep Learning | PyTorch |
| Large Language Model | Qwen2.5-3B-Instruct |
| RAG Framework | LangChain |
| Embedding Model | Sentence Transformers |
| Vector Database | FAISS |
| Document Processing | PyPDF2 |
| Deployment | Google Colab |
| Public Access | Ngrok |
| Dataset Source | Kaggle |
| Model Repository | Hugging Face |
| Email Service | Gmail SMTP |
| Version Control | Git & GitHub |


# 🧠 RAG Architecture

```text
                    PDF Documents
                          │
                          ▼
                 Document Loader
                          │
                          ▼
                  Text Chunking
                          │
                          ▼
              Sentence Embeddings
                          │
                          ▼
               FAISS Vector Store
                          │
          User Query ─────┘
                 │
                 ▼
          Similarity Search
                 │
                 ▼
        Relevant Context Retrieved
                 │
                 ▼
      Qwen2.5-3B-Instruct LLM
                 │
                 ▼
          Intelligent Final Response
```


## 📖 RAG Architecture Explanation

1. Logistics PDF documents are uploaded into the system.
2. Documents are divided into smaller chunks for efficient processing.
3. Sentence embeddings are generated for each text chunk.
4. The embeddings are stored inside a **FAISS Vector Database**.
5. User queries are converted into vector embeddings using the same embedding model.
6. FAISS performs similarity search to retrieve the most relevant document chunks.
7. The retrieved context is combined with the user's query.
8. The **Qwen2.5-3B-Instruct** Large Language Model generates an accurate, context-aware response.


# 📂 Project Structure

```text
IFQGS/
│
├── Milestone1/
│   ├── app.py
│   ├── auth.py
│   ├── database.py
│   ├── utils.py
│   ├── config.py
│   ├── requirements.txt
│   └── README.md
│
├── Milestone2/
│   ├── app.py
│   ├── llm_engine.py
│   ├── ml_models.py
│   ├── admin.py
│   ├── config.py
│   ├── requirements.txt
│   └── README.md
│
├── Milestone3/
│   ├── rag_pipeline.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── query_engine.py
│   ├── knowledge_base/
│   ├── requirements.txt
│   └── README.md
│
├── screenshots/
│
├── README.md
│
└── requirements.txt
```

---


# 🔑 Google Colab Secrets

Create the following secrets inside **Google Colab → Secrets**.

| Secret Name | Description |
|-------------|-------------|
| `NGROK_AUTHTOKEN` | Ngrok authentication token |
| `HF_TOKEN` | Hugging Face access token |
| `EMAIL_ADDRESS` | Gmail address |
| `EMAIL_PASSWORD` | Gmail App Password |
| `JWT_SECRET` | Secret key for JWT authentication |
| `KAGGLE_USERNAME` | Kaggle username |
| `KAGGLE_KEY` | Kaggle API key |

---

# 🌐 Ngrok Setup (5 Steps)

1. Create an account on the **Ngrok** website.
2. Verify your email address.
3. Copy your **Ngrok Authtoken** from the dashboard.
4. Save the token as `NGROK_AUTHTOKEN` in **Google Colab Secrets**.
5. Start Ngrok in the notebook to obtain the public **Streamlit URL**.

---

# 📊 Kaggle API Setup (5 Steps)

1. Create or log in to your **Kaggle** account.
2. Open **Account Settings**.
3. Click **Create New API Token**.
4. Download the `kaggle.json` file.
5. Save the **Kaggle Username** and **API Key** in **Google Colab Secrets**.

---

# 🤗 Hugging Face Token Setup (5 Steps)

1. Create a **Hugging Face** account.
2. Open **Settings → Access Tokens**.
3. Create a new **Read** access token.
4. Copy the generated token.
5. Store it as `HF_TOKEN` in **Google Colab Secrets**.

---

# 📧 Gmail App Password Setup (5 Steps)

1. Enable **Two-Factor Authentication (2FA)** for your Google account.
2. Open **Google Account → Security**.
3. Select **App Passwords**.
4. Generate an app password for **Mail**.
5. Save the generated 16-character password as `EMAIL_PASSWORD` in **Google Colab Secrets**.

---

# ▶️ How to Run the Project

### Step 1: Clone the Repository

```bash
git clone <repository-url>
```

### Step 2: Open in Google Colab

Open the project notebook (`.ipynb`) in **Google Colab**.

### Step 3: Configure Secrets

Add all the required secrets in **Google Colab → Secrets**.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Notebook

Execute all notebook cells sequentially.

### Step 6: Authenticate Ngrok

Configure your **Ngrok Authtoken** and start the tunnel to expose the Streamlit application.

### Step 7: Launch the Application

Run the Streamlit application from the notebook.

### Step 8: Access the Application

Open the generated **Ngrok URL** in your web browser to use the **Intelligent Freight Quote Generation System (IFQGS)**.


# 📷 Screenshots

## 🌐 Web Scraping Module

![Web Scraping](screenshots/web%20scraping.png)

The web scraping module collects relevant logistics information from web sources and extracts useful data required for building the knowledge base.

## 📚 Knowledge Base Summary

![Knowledge Base Summary](screenshots/knowledge%20base%20summary.png)

The knowledge base contains processed logistics documents and extracted information used by the RAG system for retrieving relevant context.

## 🧠 RAG Pipeline

![RAG Pipeline](screenshots/RAG%20pipeline.png)

The RAG pipeline demonstrates the complete workflow of document retrieval, similarity search, context extraction, and response generation using the LLM.

## ✅ RAG Pipeline Validation

![RAG Pipeline Validation](screenshots/RAG%20pipeline%20validation.png)

The **RAG Pipeline Validation** chart shows the evaluation results of the RAG system by representing successful (Pass) and unsuccessful (Fail) validation cases.

It verifies whether the system can retrieve relevant knowledge from the database and generate accurate, context-aware responses.
