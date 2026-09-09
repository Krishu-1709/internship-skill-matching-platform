from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import json
from services.matching import (
    calculate_match,
    calculate_readiness,
    recommend_roles
)
from services.normalizer import load_aliases, normalize_skill, normalize_role

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# Load internship data
with open("data/internships.json", "r") as file:
    internships = json.load(file)
# Load roles data
with open("data/roles.json", "r") as file:
    roles = json.load(file)
with open("data/skill_aliases.json", "r") as file:
    skill_aliases = json.load(file)

with open("data/role_aliases.json", "r") as file:
    role_aliases = json.load(file)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "roles": roles
        }
    )


@app.post("/analyze")
def analyze(
    request: Request,
    name: str = Form(...),
    education: str = Form(...),
    skills: str = Form(...),
    interests: str = Form(...),
    target_role: str = Form(...)
):

    raw_skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    student_skills = [
            normalize_skill(skill, skill_aliases)
            for skill in raw_skills
        ]

    normalized_role = normalize_role(
                target_role,
                role_aliases
            )
    role_recommendations = recommend_roles(
    student_skills,
    roles
    )   
    readiness = {
    "score": 0,
    "matched": [],
    "missing": []
}

    for role in roles:

        if role["role"].lower() == normalized_role.lower():

            readiness = calculate_readiness(
                student_skills,
                role["skills"]
            )

            break

    results = []

    for internship in internships:

        match = calculate_match(
            student_skills,
            internship["required_skills"]
        )

        results.append({
            "title": internship["title"],
            "company": internship["company"],
            "domain": internship["domain"],
            "score": match["score"],
            "matched": match["matched"],
            "missing": match["missing"]
        })

    # Highest match first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    results = results[:10]

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
        "name": name,
        "education": education,
        "skills": student_skills,
        "interests": interests,
        "target_role": normalized_role,
        "original_role": target_role,
        "readiness": readiness,
        "results": results,
        "role_recommendations": role_recommendations
    }
    )