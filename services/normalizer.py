import json


def load_aliases(filename):

    with open(filename, "r") as file:
        return json.load(file)


def normalize_skill(skill, aliases):

    cleaned = skill.strip().lower()

    return aliases.get(cleaned, skill.strip())


def normalize_role(role, aliases):

    cleaned = role.strip().lower()

    return aliases.get(cleaned, role.strip())