from data import JOB_ROLES


def recommend_roles(candidate_information):

    candidate_items = set()

    for item in candidate_information["skills"]:
        candidate_items.add(item.lower())

    for item in candidate_information["technologies"]:
        candidate_items.add(item.lower())

    for item in candidate_information["languages"]:
        candidate_items.add(item.lower())

    recommendations = []

    for role, requirements in JOB_ROLES.items():

        matched = []

        for requirement in requirements:

            if requirement.lower() in candidate_items:
                matched.append(requirement)

        if len(requirements) > 0:
            score = (len(matched) / len(requirements)) * 100
        else:
            score = 0

        recommendations.append({
            "role": role,
            "score": round(score, 2),
            "matched": matched
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations


def calculate_job_match(
    candidate_information,
    job_information
):

    candidate_skills = {
        item.lower()
        for item in candidate_information["skills"]
    }

    candidate_technologies = {
        item.lower()
        for item in candidate_information["technologies"]
    }

    candidate_languages = {
        item.lower()
        for item in candidate_information["languages"]
    }

    job_skills = {
        item.lower()
        for item in job_information["skills"]
    }

    job_technologies = {
        item.lower()
        for item in job_information["technologies"]
    }

    job_languages = {
        item.lower()
        for item in job_information["languages"]
    }

    # Find matches
    matched_skills = candidate_skills.intersection(
        job_skills
    )

    matched_technologies = candidate_technologies.intersection(
        job_technologies
    )

    matched_languages = candidate_languages.intersection(
        job_languages
    )

    # Calculate individual scores
    if job_skills:
        skill_score = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        skill_score = 100

    if job_technologies:
        technology_score = (
            len(matched_technologies)
            / len(job_technologies)
        ) * 100
    else:
        technology_score = 100

    if job_languages:
        language_score = (
            len(matched_languages)
            / len(job_languages)
        ) * 100
    else:
        language_score = 100

    # Weighted final score
    final_score = (
        skill_score * 0.40
        + technology_score * 0.35
        + language_score * 0.25
    )

    missing_skills = job_skills - candidate_skills

    missing_technologies = (
        job_technologies - candidate_technologies
    )

    missing_languages = (
        job_languages - candidate_languages
    )

    return {
        "score": round(final_score, 2),

        "matched_skills": sorted(matched_skills),

        "matched_technologies": sorted(
            matched_technologies
        ),

        "matched_languages": sorted(
            matched_languages
        ),

        "missing_skills": sorted(
            missing_skills
        ),

        "missing_technologies": sorted(
            missing_technologies
        ),

        "missing_languages": sorted(
            missing_languages
        )
    }