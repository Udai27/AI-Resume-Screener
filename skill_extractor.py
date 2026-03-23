from skills import SKILLS

def extract_skills(text):
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
def calculate_skill_match(resume_skills, jd_skills):
    if not jd_skills:
        return 0

    matched = set(resume_skills) & set(jd_skills)
    return round((len(matched) / len(jd_skills)) * 100, 2)