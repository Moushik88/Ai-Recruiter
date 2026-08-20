# AI Recruiter — NLP + ChatBot Track

## Project Overview

AI Recruiter is an NLP-powered recruitment assistant that extracts structured candidate information (skills, technologies, programming languages) from conversational text and resumes — including scanned/image-based resumes via OCR — and matches candidates to suitable job roles and job descriptions. No LLM API is used anywhere in the pipeline; all extraction and matching relies on classical, fully explainable NLP techniques.

## Problem Statement

Recruiters deal with unstructured input: free-text candidate descriptions, PDF resumes, and even scanned/image resumes that aren't machine-readable by default. Manually reading and matching these against job requirements is slow and inconsistent. This project automates:

1. Extracting skills, technologies, and languages from free text and resumes (including OCR for scanned/image resumes)
2. Recommending the most suitable job roles for a candidate, ranked by score
3. Matching a candidate against a specific job description with a weighted match score, showing what's matched and what's missing

## Installation Instructions

```bash
# Clone the repo
git clone <your-repo-url>
cd ai-recruiter

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\\\\Scripts\\\\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (required for scanned/image resume support)
# Windows: download installer from https://github.com/UB-Mannheim/tesseract/wiki
# and update the path in app.py (pytesseract.pytesseract.tesseract\\\_cmd)
# Mac: brew install tesseract
# Linux: sudo apt install tesseract-ocr

# Run the app
python -m streamlit run app.py
```

## Dataset Used

* No dataset was mandated for this track.
* Gazetteer word lists (skills, technologies, languages) were manually curated to cover common AI/ML, software, and general professional terms, used as the reference vocabulary for extraction.
* \[FILL IN: if you tested against any external sample resumes/JDs, name the source here]

## Methodology

**Part 1 — Extraction (`extractor.py`)**

* Input text (conversational or resume-derived) is matched against curated skill/technology/language word lists to identify relevant terms.
* Output is returned as structured data: skills, technologies, and languages found in the text.
* The same extraction logic is reused for both raw conversational input and parsed resume text, so Part 1 and Part 2 share one consistent extraction pipeline.

**Part 2 — Resume Parsing \& OCR**

* Text-based PDF resumes are parsed directly using `pymupdf`.
* Scanned/image-based resumes (where no text layer exists) are handled via OCR using `pytesseract`, converting the image content to raw text before running it through the same extractor.
* JPG/PNG resume uploads are supported the same way.
* Since OCR output can contain misreads (e.g. "leveloper" instead of "developer"), a lightweight text-cleaning step corrects a set of common OCR errors *for display purposes only* — the underlying extraction always runs on the original OCR text, so correction mistakes can't silently change what's detected.

**Part 2 — Job Role Recommendation (`matcher.py`)**

* A reference table maps job roles to representative skill/technology/language sets.
* Candidate data extracted from a resume is compared against each role, and a score is computed.
* Only roles with a non-zero score are shown, ranked and capped at the top 5, so recruiters see relevant suggestions instead of a full list padded with 0% matches.

**Part 2 — Weighted Job-Description Matching**

* When matching a candidate against a specific job description, not all categories are treated equally — technical requirements carry more weight than general skills:

  * Skills: 40%
  * Technologies: 35%
  * Programming languages: 25%
* For each category, the match percentage is the proportion of the job's required terms found in the candidate's extracted terms. The final score is the weighted sum of the three category scores.
* The output includes the overall score plus explicit matched and missing items per category (skills, technologies, languages), so the reasoning behind the score is fully visible rather than a single opaque number.

**Why not an LLM?**
The challenge explicitly disallows LLM API usage for this track. A rule-based extraction + weighted scoring approach was chosen deliberately because every extraction and every point of the match score can be traced back to a specific term comparison — there's no black-box step, which matters for the "Understanding \& Explanation" evaluation criterion.

## Technologies Used

* Python
* Streamlit — interactive dashboard UI
* PyMuPDF (`pymupdf`) — text-based PDF resume parsing
* pytesseract + Tesseract OCR — scanned/image resume text extraction
* Pillow (`PIL`) — image handling for OCR input

## Results

The application was validated with a systematic test plan covering both normal and edge-case inputs:

|Test|Scenario|Result|
|-|-|-|
|1|Candidate extraction from conversational text|\[FILL IN: pass/fail + what was detected]|
|2|Text-based PDF resume upload|\[FILL IN: pass/fail]|
|3|Scanned/image resume upload (OCR)|\[FILL IN: pass/fail, note any OCR quirks]|
|4|Resume matched against a closely related job description|\[FILL IN: match score achieved, e.g. matched Python/ML/SQL/Git]|
|5|Same resume matched against an unrelated job description (Java/Spring Boot role)|\[FILL IN: confirm score was noticeably lower than Test 4]|
|6|Empty inputs (no text / no resume / no job description)|\[FILL IN: confirm appropriate warnings shown, no crash]|

Sample outputs:

* Input: `"I worked in the AI/ML Department and worked with CNN Models using Python"` →
Output: `{"skill": \\\["AI/ML"], "technology": \\\["CNN"], "language": \\\["Python"]}`
* \[FILL IN: one real match-score example from your app, e.g. "Resume vs. Python/ML job description → 78.5% match, with matched skills, technologies, languages, and missing requirements listed"]
* \[FILL IN: one real top-5 role recommendation example]

## Challenges Faced

* OCR output from scanned resumes was noisy and contained misspelled words (e.g. "sottware", "zecurity"), which required a dedicated cleaning step for display without corrupting the actual extraction input.
* Treating all extracted terms equally gave misleading match scores (e.g. a general skill like "communication" counted the same as a critical technical requirement like "Python"), which is why weighted scoring by category was introduced.
* Showing every job role — including ones with 0% relevance — cluttered the recommendation output, so results were filtered and capped to the top matches only.
* \[FILL IN: any other specific issues you ran into, e.g. Tesseract path/config issues, PDF parsing edge cases]

## Future Improvements

* Expand the gazetteer with a larger, more comprehensive skills/technology taxonomy
* Improve OCR correction with a proper spell-checker instead of a fixed replacement list
* Add multilingual resume support
* Allow adjustable category weights (skills/technologies/languages) depending on the role type
* Add conversation memory for a more chatbot-like interaction flow

