import re
import spacy
import streamlit as st
import spacy

@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(tokens)