import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model only once
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


def calculate_batch_similarity(resume_texts, job_description):
    """
    resume_texts → list of resumes (strings)
    job_description → single string
    """

    # Encode JD once
    jd_embedding = model.encode([job_description])

    # Encode all resumes together (batch)
    resume_embeddings = model.encode(resume_texts)

    scores = cosine_similarity(resume_embeddings, jd_embedding)

    return [round(float(score[0]) * 100, 2) for score in scores]