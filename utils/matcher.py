from utils.skill_extractor import extract_skills

def calculate_match(resume_text, job_description):

    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))

    matched = list(resume_skills.intersection(jd_skills))
    missing = list(jd_skills - resume_skills)

    if len(jd_skills) == 0:
        score = 0
    else:
        score = round(
            (len(matched) / len(jd_skills)) * 100,
            2
        )

    return score, matched, missing