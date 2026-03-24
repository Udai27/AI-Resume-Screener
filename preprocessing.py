# import re
# # import spacy
# import streamlit as st

# @st.cache_resource
# def load_spacy_model():
#     return spacy.load("en_core_web_sm")

# nlp = load_spacy_model()

# def clean_text(text):
#     text = text.lower()
#     text = re.sub(r'\W+', ' ', text)
#     return text

# # def preprocess_text(text):
# #     doc = nlp(text)
# #     tokens = [token.lemma_ for token in doc if not token.is_stop]
# #     return " ".join(tokens)

# def preprocess_text(text):
#     text = text.lower()
#     text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
#     return text

import re

# Clean text
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

# Simple preprocessing (no spaCy)
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    words = text.split()
    return " ".join(words)