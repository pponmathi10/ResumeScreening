import streamlit as st
import PyPDF2
import pandas as pd
from io import BytesIO

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Recruiter ATS Screening", layout="wide")
st.title("🧑‍💼 Recruiter ATS Resume Screening")
st.caption("Open Login | Bulk Resume Screening | Excel Output")

# --------------------------------------------------
# CSS for professional dark + teal accent theme
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #0b132b, #1c2541, #00b4d8);
    background-attachment: fixed;
    color: #eaeaea;
}
.block-container { padding-top: 1rem; }

h1, h2, h3 {
    color: #ffffff;
    text-shadow: none;
}

.card {
    background: rgba(11,19,43,0.9);
    border: 1px solid rgba(0,180,216,0.35);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}

.metric {
    background: rgba(11,19,43,0.95);
    border: 1px solid #00b4d8;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}

.selected { color: #00ff9c; font-size: 20px; font-weight: 600; }
.rejected { color: #ff6b6b; font-size: 20px; font-weight: 600; }

.skill {
    display: inline-block; padding: 7px 14px; margin: 4px;
    border-radius: 18px; background: rgba(0,180,216,0.15);
    border: 1px solid rgba(0,180,216,0.5); color: #eafcff;
}
.missing {
    border-color: #ff6b6b; background: rgba(255,107,107,0.15); color: #ffeaea;
}

.tip {
    border-left: 4px solid #00b4d8;
    padding: 12px; margin-bottom: 10px;
    background: rgba(11,19,43,0.85); border-radius: 10px;
}

.stButton>button {
    background: linear-gradient(90deg, #00b4d8, #48cae4);
    color: #001219; font-weight: 600; padding: 12px 28px;
    border-radius: 10px; border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #48cae4, #00b4d8);
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "recruiter_name" not in st.session_state:
    st.session_state.recruiter_name = ""

# --------------------------------------------------
# Job Roles & Skills
# --------------------------------------------------
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "pandas", "numpy", "scikit-learn"]
    }
}

# --------------------------------------------------
# PDF Reader
# --------------------------------------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# --------------------------------------------------
# Resume Evaluation with Main Skill & 50% logic
# --------------------------------------------------
def evaluate_resume(text, role, jd=None):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]

    score = int((len(matched)/len(skills))*100)

    # Decision Logic
