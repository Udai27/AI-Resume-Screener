# =========================
# 1. IMPORTS
# =========================
import streamlit as st
import pandas as pd
import math
import plotly.express as px
import csv

from preprocessing import clean_text, preprocess_text
from skill_extractor import extract_skills, calculate_skill_match
from resume_parser import extract_text_from_pdf
from semantic_similarity import calculate_batch_similarity
from similarity import calculate_tfidf_similarity
from hybrid_score import calculate_hybrid_score
from job_api import fetch_job_description

# =========================
# 2. AUTH FUNCTIONS
# =========================
def authenticate(username, password):
    try:
        df = pd.read_csv("login_data.csv")
        user = df[(df["username"] == username) & (df["password"] == password)]
        return not user.empty
    except:
        return False

def register_user(username, password):
    try:
        df = pd.read_csv("login_data.csv")
    except:
        df = pd.DataFrame(columns=["username", "password"])

    if username in df["username"].values:
        return False

    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv("login_data.csv", index=False)
    return True

# =========================
# 3. LOGIN + SIGNUP UI
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

def load_login_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #020617);
    }

    .auth-box {
    padding: 40px;
    width: 350px;
    margin: auto;
    margin-top: 8%;
    text-align: center;
}

    .logo-box {
        background: #0f172a;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        font-size: 20px;
        font-weight: bold;
        color: #38bdf8;
        text-align: center;

        box-shadow: 0px 0px 20px rgba(56,189,248,0.5),
                    0px 0px 40px rgba(56,189,248,0.3);
    }

    .title {
        font-size: 22px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 15px;
    }

    .stButton>button {
        width: 100%;
        background: #38bdf8;
        color: black;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

load_login_css()

if not st.session_state.logged_in:

    st.markdown('<div class="auth-box">', unsafe_allow_html=True)

    # 🔥 GLOWING TITLE
    st.markdown("""
    <div class="logo-box">
        🚀 AI Resume Screener
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="title">{st.session_state.auth_mode}</div>', unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.session_state.auth_mode == "Login":

        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("New user? Signup here"):
            st.session_state.auth_mode = "Signup"
            st.rerun()

    else:
        if st.button("Create Account"):
            if register_user(username, password):
                st.success("Account created! Please login.")
                st.session_state.auth_mode = "Login"
                st.rerun()
            else:
                st.error("Username already exists")

        if st.button("Already have account? Login"):
            st.session_state.auth_mode = "Login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =========================
# 4. PAGE CONFIG
# =========================
st.set_page_config(page_title="SmartHire AI", page_icon="🚀", layout="wide")

# =========================
# 5. MAIN UI
# =========================
st.markdown("<h1 style='text-align:center;'>🚀 SmartHire AI Resume Screener</h1>", unsafe_allow_html=True)

st.sidebar.title("⚙️ Settings")
top_n = st.sidebar.slider("Top Candidates", 1, 20, 5)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# =========================
# INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    input_mode = st.selectbox(
        "Select Input Type",
        ["Upload PDF Files", "Upload CSV Dataset"]
    )

    if input_mode == "Upload PDF Files":
        uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    else:
        csv_file = st.file_uploader("Upload CSV", type="csv")

with col2:
    job_role = st.text_input("💼 Enter Job Role")

check_button = st.button("🚀 Analyze")

# =========================
# LOGIC
# =========================
if check_button:

    resume_texts = []
    candidate_names = []

    if input_mode == "Upload CSV Dataset":
        if not csv_file:
            st.warning("Upload CSV first")
            st.stop()

        dataset = pd.read_csv(csv_file)

        if job_role:
            dataset = dataset[
                dataset["Category"].astype(str).str.lower().str.contains(job_role.lower(), na=False)
            ]

        if dataset.empty:
            st.error("No matching resumes found")
            st.stop()

        resume_texts = dataset["Resume_str"].astype(str).tolist()
        candidate_names = dataset["ID"].astype(str).tolist()

    else:
        if not uploaded_files:
            st.warning("Upload PDFs first")
            st.stop()

        for file in uploaded_files:
            text = extract_text_from_pdf(file)
            text = preprocess_text(clean_text(text))
            resume_texts.append(text)
            candidate_names.append(file.name)

    if not job_role:
        st.warning("Enter job role")
        st.stop()

    with st.spinner("Fetching job data..."):
        jd = fetch_job_description(job_role)

    jd = preprocess_text(clean_text(jd))

    st.subheader("⚡ Processing Resumes...")

    semantic_scores = calculate_batch_similarity(resume_texts, jd)

    results = []

    for i, resume in enumerate(resume_texts):
        tfidf = calculate_tfidf_similarity(resume, jd)

        res_skills = extract_skills(resume)
        jd_skills = extract_skills(jd)

        skill_score = calculate_skill_match(res_skills, jd_skills)

        final_score = calculate_hybrid_score(
            semantic_scores[i], tfidf, skill_score
        )

        results.append({
            "Candidate": candidate_names[i],
            "Score": final_score
        })

    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

    # =========================
    # RESULTS
    # =========================
    st.subheader("🏆 Top Candidates")

    for _, row in df.head(top_n).iterrows():
        st.markdown(f"""
        <div style="background:#1e293b;padding:15px;border-radius:10px;margin-bottom:10px;">
            <h3>{row['Candidate']}</h3>
            <p>Score: <b>{row['Score']}%</b></p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📊 Full Ranking")
    st.dataframe(df, use_container_width=True)

    # =========================
    # GRAPHS
    # =========================
    st.subheader("📊 Visual Insights")

    top_df = df.head(top_n)

    st.plotly_chart(px.bar(top_df, x="Candidate", y="Score", title="Top Candidates"), use_container_width=True)
    st.plotly_chart(px.pie(top_df, names="Candidate", values="Score", title="Score Distribution"), use_container_width=True)
    st.plotly_chart(px.histogram(df, x="Score", nbins=10, title="Score Spread"), use_container_width=True)

    # =========================
    # METRICS
    # =========================
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", len(df))
    col2.metric("Top Score", f"{df.iloc[0]['Score']}%")
    col3.metric("Avg Score", f"{round(df['Score'].mean(),2)}%")

    st.success(f"🎯 Best Candidate: {df.iloc[0]['Candidate']}")