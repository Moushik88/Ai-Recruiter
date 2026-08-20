from data import SKILLS, TECHNOLOGIES, LANGUAGES


def clean_ocr_text(text):
    """Fix common OCR mistakes."""

    replacements = {
        "sottware": "software",
        "leveloper": "developer",
        "zecurity": "security",
        "curity": "security",
        "azzisted": "assisted",
        "proje": "project",
        "scHooL": "school",
        "high schoo!": "high school",
    }

    text = text.lower()

    for wrong, correct in replacements.items():
        text = text.replace(wrong.lower(), correct.lower())

    return text


def extract_information(text):

    text = clean_ocr_text(text)

    skills = []
    technologies = []
    languages = []

    # -----------------------------------------
    # NORMAL KEYWORD MATCHING
    # -----------------------------------------

    for skill in SKILLS:
        if skill.lower() in text:
            skills.append(skill)

    for technology in TECHNOLOGIES:
        if technology.lower() in text:
            technologies.append(technology)

    for language in LANGUAGES:
        if language.lower() in text:
            languages.append(language)

    # -----------------------------------------
    # RESUME-SPECIFIC PHRASES
    # -----------------------------------------

    if "software developer" in text:
        if "software development" not in skills:
            skills.append("software development")

    if "senior software developer" in text:
        if "software engineering" not in skills:
            skills.append("software engineering")

    if "junior software developer" in text:
        if "software development" not in skills:
            skills.append("software development")

    if "led a team" in text:
        if "leadership" not in skills:
            skills.append("leadership")

    if "collaborated with the team" in text:
        if "teamwork" not in skills:
            skills.append("teamwork")

    if "computer science" in text:
        if "computer science" not in skills:
            skills.append("computer science")

    if "cybersecurity" in text:
        if "cybersecurity" not in skills:
            skills.append("cybersecurity")

    return {
        "skills": skills,
        "technologies": technologies,
        "languages": languages
    }