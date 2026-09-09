def calculate_match(student_skills, required_skills):

    student_skills = {
        skill.strip().lower()
        for skill in student_skills
    }

    required_skills = {
        skill.strip().lower()
        for skill in required_skills
    }

    matched = student_skills.intersection(required_skills)
    missing = required_skills - student_skills

    if len(required_skills) == 0:
        score = 0
    else:
        score = (len(matched) / len(required_skills)) * 100

    return {
        "score": round(score),
        "matched": sorted(matched),
        "missing": sorted(missing)
    }
def calculate_readiness(student_skills, required_skills):

    student = {
        skill.strip().lower()
        for skill in student_skills
    }

    required = {
        skill.strip().lower()
        for skill in required_skills
    }

    matched = student.intersection(required)
    missing = required - student

    if len(required) == 0:
        score = 0
    else:
        score = (len(matched) / len(required)) * 100

    return {
        "score": round(score),
        "matched": sorted(matched),
        "missing": sorted(missing)
    }

def recommend_roles(student_skills, roles):
    results = []

    for role in roles:

        match = calculate_match(
            student_skills,
            role["skills"]
        )

        result = {
            "role": role["role"],
            "score": match["score"],
            "matched": match["matched"],
            "missing": match["missing"]
        }

        result["level"] = get_match_level(result["score"])
        result["reason"] = generate_reason(result)

        results.append(result)

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    results = results[:10]

    for index, result in enumerate(results, start=1):
        result["priority"] = index

    return results
def get_match_level(score):

    if score >= 80:
        return "Strong Match"

    elif score >= 60:
        return "Good Match"

    else:
        return "Explore"
def generate_reason(role):
    matched = role["matched"]
    missing = role["missing"]

    if len(matched) >= 4:
        return f"Strong match because you already have {', '.join(matched[:4])}."

    elif len(matched) >= 2:
        return f"Good match because you already have {', '.join(matched[:3])}."

    else:
        return "This role may be worth exploring based on your current profile."