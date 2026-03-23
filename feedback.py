def generate_feedback(final_score, skill_score, missing_skills):
    
    feedback = []

    if final_score > 80:
        feedback.append("Excellent match for the role.")
    elif final_score > 60:
        feedback.append("Good match, but improvement needed.")
    else:
        feedback.append("Low match. Significant improvement required.")

    if skill_score < 50:
        feedback.append("Improve skill alignment with job requirements.")

    if missing_skills:
        feedback.append(
            "Consider adding experience in: " + ", ".join(missing_skills)
        )

    return feedback