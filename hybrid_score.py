def calculate_hybrid_score(semantic_score, tfidf_score, skill_score):
    final_score = (
        0.5 * semantic_score +
        0.3 * tfidf_score +
        0.2 * skill_score
    )
    return round(final_score, 2)