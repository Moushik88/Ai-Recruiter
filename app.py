import streamlit as st
import pymupdf
import pytesseract

from PIL import Image

from extractor import extract_information
from matcher import recommend_roles, calculate_job_match


# ==================================================
# CONFIGURATION
# ==================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


st.set_page_config(
    page_title="AI Recruiter",
    page_icon="🤖",
    layout="wide"
)
# ==================================================
# CUSTOM UI STYLING
# ==================================================

st.markdown(
    """
    <style>

    /* Main application */

    .main {
        padding-top: 1rem;
    }


    /* Main title */

    h1 {
        font-size: 42px;
        font-weight: 700;
    }


    /* Section headings */

    h2 {
        margin-top: 25px;
        font-weight: 650;
    }


    /* Subheadings */

    h3 {
        font-weight: 600;
    }


    /* Metric cards */

    [data-testid="stMetric"] {

        background-color: rgba(128, 128, 128, 0.08);

        border-radius: 12px;

        padding: 15px;

        border: 1px solid rgba(128, 128, 128, 0.15);
    }


    /* Buttons */

    .stButton > button {

        width: 100%;

        border-radius: 8px;

        font-weight: 600;

        padding: 0.6rem 1rem;
    }


    /* Text areas */

    textarea {

        border-radius: 8px !important;
    }


    /* File uploader */

    [data-testid="stFileUploader"] {

        border-radius: 10px;
    }


    /* Progress bars */

    [data-testid="stProgressBar"] {

        margin-top: 8px;

        margin-bottom: 15px;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# OCR TEXT CLEANING
# ==================================================

def clean_display_text(text):

    replacements = {
        "leveloper": "developer",
        "sottware": "software",
        "zecurity": "security",
        "curity": "security",
        "azzisted": "assisted",
        "proje": "project",
        "schoo!": "school",
        "scHooL": "school",
        "learnlng": "learning",
        "machlne": "machine"
    }

    cleaned_text = text

    for wrong, correct in replacements.items():

        cleaned_text = cleaned_text.replace(
            wrong,
            correct
        )

        cleaned_text = cleaned_text.replace(
            wrong.capitalize(),
            correct.capitalize()
        )

        cleaned_text = cleaned_text.replace(
            wrong.upper(),
            correct.upper()
        )

    return cleaned_text


# ==================================================
# PDF TEXT EXTRACTION
# ==================================================

def extract_text_from_pdf(file):

    complete_text = ""

    pdf_document = pymupdf.open(
        stream=file.read(),
        filetype="pdf"
    )

    for page in pdf_document:

        # Try normal text extraction
        page_text = page.get_text()

        if page_text.strip():

            complete_text += page_text + "\n"

        else:

            # Scanned/image-based page
            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2)
            )

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            ocr_text = pytesseract.image_to_string(
                image
            )

            complete_text += ocr_text + "\n"

    pdf_document.close()

    return complete_text


# ==================================================
# IMAGE TEXT EXTRACTION
# ==================================================

def extract_text_from_image(file):

    image = Image.open(file)

    text = pytesseract.image_to_string(
        image
    )

    return text


# ==================================================
# TITLE
# ==================================================

st.title("🤖 AI Recruiter")

st.markdown(
    """
    ### AI-Powered Resume Screening & Job Matching

    Analyze resumes, extract candidate skills, recommend suitable
    job roles, and compare candidates with job requirements.
    """
)

st.divider()


# ==================================================
# PART 1
# ==================================================

st.header(
    "Part 1 - Candidate Information Extraction"
)


experience_text = st.text_area(
    "Describe your experience:",
    height=150,
    placeholder=(
        "Example: I worked with CNN models "
        "using Python and machine learning."
    )
)


if st.button("Extract Information"):

    if experience_text.strip():

        try:

            result = extract_information(
                experience_text
            )

            st.subheader(
                "Extracted Information"
            )

            st.json(result)

        except Exception as error:

            st.error(
                f"An error occurred: {error}"
            )

    else:

        st.warning(
            "Please enter some experience information."
        )


# ==================================================
# PART 2 - RESUME ANALYSIS
# ==================================================

st.header(
    "Part 2 - Resume Analysis"
)


uploaded_file = st.file_uploader(
    "Upload your resume (PDF or Image)",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg"
    ]
)


resume_text = ""


# ==================================================
# PROCESS RESUME
# ==================================================

if uploaded_file is not None:

    try:

        if uploaded_file.type == "application/pdf":

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        else:

            resume_text = extract_text_from_image(
                uploaded_file
            )


        # ------------------------------------------
        # DISPLAY CLEANED RESUME TEXT
        # ------------------------------------------

        st.subheader(
            "📄 Extracted Resume Text"
        )


        if resume_text.strip():

            cleaned_resume_text = (
                clean_display_text(resume_text)
            )

            st.text_area(
                "Processed resume content:",
                cleaned_resume_text,
                height=350
            )

        else:

            st.warning(
                "No text could be extracted from this resume."
            )


    except Exception as error:

        st.error(
            "An error occurred while processing "
            f"the resume: {error}"
        )


# ==================================================
# ANALYZE RESUME
# ==================================================

if st.button("Analyze Resume"):

    if resume_text.strip():

        try:

            # --------------------------------------
            # CANDIDATE INFORMATION
            # --------------------------------------

            result = extract_information(
                resume_text
            )


            st.subheader(
                "👤 Extracted Candidate Information"
            )


            # --------------------------------------
            # SUMMARY CARDS
            # --------------------------------------

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Skills",
                    len(result["skills"])
                )


            with col2:

                st.metric(
                    "Technologies",
                    len(result["technologies"])
                )


            with col3:

                st.metric(
                    "Languages",
                    len(result["languages"])
                )


            # --------------------------------------
            # SKILLS
            # --------------------------------------

            st.write("### 🧠 Skills")


            if result["skills"]:

                for skill in result["skills"]:

                    st.write(
                        f"✅ {skill}"
                    )

            else:

                st.write(
                    "No skills detected."
                )


            # --------------------------------------
            # TECHNOLOGIES
            # --------------------------------------

            st.write(
                "### 💻 Technologies"
            )


            if result["technologies"]:

                for technology in result[
                    "technologies"
                ]:

                    st.write(
                        f"✅ {technology}"
                    )

            else:

                st.write(
                    "No technologies detected."
                )


            # --------------------------------------
            # PROGRAMMING LANGUAGES
            # --------------------------------------

            st.write(
                "### 🧑‍💻 Programming Languages"
            )


            if result["languages"]:

                for language in result[
                    "languages"
                ]:

                    st.write(
                        f"✅ {language}"
                    )

            else:

                st.write(
                    "No programming languages detected."
                )


            # ==================================================
            # JOB ROLE RECOMMENDATION
            # ==================================================

            st.subheader(
                "🎯 Recommended Job Roles"
            )


            recommendations = recommend_roles(
                result
            )

            recommendations = [
                recommendation
                for recommendation in recommendations
                if recommendation["score"] > 0
            ][:5]


            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                role = recommendation["role"]

                score = recommendation["score"]

                matched = recommendation["matched"]


                st.write(
                    f"### {index}. {role}"
                )


                st.progress(
                    min(int(score), 100),
                    text=f"Match: {score}%"
                )


                if matched:

                    st.write(
                        "Matched:",
                        ", ".join(matched)
                    )

                else:

                    st.write(
                        "Matched: None"
                    )


        except Exception as error:

            st.error(
                "An error occurred while analyzing "
                f"the resume: {error}"
            )

    else:

        st.error(
            "Please upload a resume first."
        )


# ==================================================
# PART 2C - JOB DESCRIPTION MATCHING
# ==================================================

st.header(
    "Part 2C - Job Description Matching"
)


job_description = st.text_area(
    "Paste the Job Description here:",
    height=250,
    placeholder=(
        "Example: We are looking for a Python "
        "developer with experience in machine "
        "learning, SQL, Git, Docker and TensorFlow."
    )
)


if st.button("Match Candidate with Job"):

    if resume_text.strip() and job_description.strip():

        try:

            # --------------------------------------
            # EXTRACT JOB INFORMATION
            # --------------------------------------

            job_information = extract_information(
                job_description
            )


            st.subheader(
                "📋 Extracted Job Requirements"
            )


            # --------------------------------------
            # JOB REQUIREMENT SUMMARY
            # --------------------------------------

            job_col1, job_col2, job_col3 = st.columns(3)


            with job_col1:

                st.metric(
                    "Required Skills",
                    len(job_information["skills"])
                )


            with job_col2:

                st.metric(
                    "Technologies",
                    len(job_information["technologies"])
                )


            with job_col3:

                st.metric(
                    "Languages",
                    len(job_information["languages"])
                )


            # --------------------------------------
            # CANDIDATE INFORMATION
            # --------------------------------------

            candidate_information = (
                extract_information(resume_text)
            )


            # --------------------------------------
            # CALCULATE MATCH
            # --------------------------------------

            match_result = calculate_job_match(
                candidate_information,
                job_information
            )


            score = match_result["score"]


            # --------------------------------------
            # MATCH SCORE
            # --------------------------------------

            st.subheader(
                "🎯 Candidate - Job Match"
            )


            st.metric(
                "Overall Match Score",
                f"{score}%"
            )


            st.progress(
                min(int(score), 100)
            )


            # --------------------------------------
            # MATCHED SKILLS
            # --------------------------------------

            st.subheader(
                "✅ Matched Skills"
            )


            if match_result[
                "matched_skills"
            ]:

                for item in match_result[
                    "matched_skills"
                ]:

                    st.write(
                        f"✅ {item}"
                    )

            else:

                st.write(
                    "No matching skills found."
                )


            # --------------------------------------
            # MATCHED TECHNOLOGIES
            # --------------------------------------

            st.subheader(
                "💻 Matched Technologies"
            )


            if match_result[
                "matched_technologies"
            ]:

                for item in match_result[
                    "matched_technologies"
                ]:

                    st.write(
                        f"✅ {item}"
                    )

            else:

                st.write(
                    "No matching technologies found."
                )


            # --------------------------------------
            # MATCHED LANGUAGES
            # --------------------------------------

            st.subheader(
                "🧑‍💻 Matched Programming Languages"
            )


            if match_result[
                "matched_languages"
            ]:

                for item in match_result[
                    "matched_languages"
                ]:

                    st.write(
                        f"✅ {item}"
                    )

            else:

                st.write(
                    "No matching languages found."
                )


            # --------------------------------------
            # MISSING REQUIREMENTS
            # --------------------------------------

            st.subheader(
                "❌ Missing Requirements"
            )


            missing_found = False


            for item in match_result[
                "missing_skills"
            ]:

                st.write(
                    f"❌ {item}"
                )

                missing_found = True


            for item in match_result[
                "missing_technologies"
            ]:

                st.write(
                    f"❌ {item}"
                )

                missing_found = True


            for item in match_result[
                "missing_languages"
            ]:

                st.write(
                    f"❌ {item}"
                )

                missing_found = True


            if not missing_found:

                st.success(
                    "The candidate meets all detected requirements!"
                )


        except Exception as error:

            st.error(
                "An error occurred while matching: "
                f"{error}"
            )


    elif not resume_text.strip():

        st.warning(
            "Please upload a resume first."
        )


    else:

        st.warning(
            "Please enter a job description."
        )