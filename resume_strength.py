def calculate_resume_strength(resume_text, skills_found):
    score = 0

    # Skill count weight
    score += len(skills_found) * 5

    # Bonus keywords
    bonus_keywords = [
        "project", "internship", "experience",
        "machine learning", "deep learning",
        "data analysis", "research"
    ]

    for word in bonus_keywords:
        if word in resume_text:
            score += 5

    # Cap score at 100
    return min(score, 100)