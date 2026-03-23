# 🚀 SmartHire – AI Resume Screening System

SmartHire is an AI-powered Resume Screening System that automates candidate evaluation using Hybrid AI scoring techniques.

It supports both **PDF resume uploads** and **CSV dataset ingestion**, integrates live job requirements using API-based fetching, and ranks candidates using a multi-layered evaluation model.

---

## 🔥 Features

✅ Multi-source resume input (PDF & CSV)  
✅ Live Job Role fetching via Job API  
✅ Hybrid AI Scoring Model:
- Semantic Similarity (Sentence Transformers)
- TF-IDF Similarity
- Skill Matching Score
✅ Resume Strength Analysis (Single Resume Mode)  
✅ AI-based Candidate Ranking Dashboard  
✅ Clean Streamlit UI  
✅ Secure API key handling (.env based)

---

## 🧠 Hybrid Scoring Architecture

Final Score = Weighted Combination of:

- **Semantic Score** (Transformer-based meaning similarity)
- **TF-IDF Score** (Keyword-level similarity)
- **Skill Match Score** (Extracted skill overlap)

This ensures both contextual understanding and keyword precision.

---

## 🏗️ Project Structure
AI-Resume-Screener/
│
├── app.py
├── job_api.py
├── semantic_similarity.py
├── similarity.py
├── skill_extractor.py
├── hybrid_score.py
├── resume_strength.py
├── feedback.py
├── preprocessing.py
├── requirements.txt
├── .gitignore
└── README.md

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
git clone https://github.com/Udai27/AI-Resume-Screener.git

cd AI-Resume-Screener

### 2️⃣ Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt


### 4️⃣ Setup Environment Variables

Create a `.env` file:
ADZUNA_APP_ID=your_app_id
ADZUNA_API_KEY=your_api_key

---

## ▶️ Run Application
streamlit run app.py

---

## 🧪 Testing Modes

### 📄 Single Resume Mode
- Upload one PDF
- Get resume strength score

### 🏆 Screening Mode
- Upload multiple resumes
- Enter job role
- Get ranked candidate dashboard

### 📊 CSV Dataset Mode
- Upload structured resume dataset
- Automatically filter by job category
- Rank candidates instantly

---

## 🔐 Security

- API keys stored using environment variables
- `.env` excluded via `.gitignore`
- Virtual environment excluded from repository

---

## 🚀 Future Improvements

- Resume feedback generation using LLM
- Candidate shortlisting automation
- Admin dashboard analytics
- Cloud deployment (Streamlit Cloud / Render)

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Sentence Transformers (MiniLM)
- Scikit-learn
- Pandas
- Requests

---

## 👨‍💻 Author

Developed by Udai Veer Yadav  
B.Tech CSE | AI & Software Systems Enthusiast

---

## 📌 License

This project is for educational and demonstration purposes.

