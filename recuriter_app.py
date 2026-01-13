import streamlit as st
import PyPDF2
import pandas as pd
from io import BytesIO

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Recruiter ATS Screening", layout="wide")
st.title("Recruiter ATS Resume Screening")
st.caption("Open Login | Bulk Resume Screening | Excel Output")

# --------------------------------------------------
# Professional Dark Theme (NO NEON TITLE)
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b132b, #1c2541, #00b4d8);
    background-attachment: fixed;
    color: white;
}
h1,h2,h3 { color: white; text-shadow: none; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "recruiter_name" not in st.session_state:
    st.session_state.recruiter_name = ""
if "results_df" not in st.session_state:
    st.session_state.results_df = None

# --------------------------------------------------
# Job Roles
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
# Resume Evaluation Logic
# --------------------------------------------------
def evaluate_resume(text, role):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]
    score = int(len(matched) / len(skills) * 100)

    if main_skill in text or score >= 50:
        decision = "SELECT"
        status = "Hired"
    else:
        decision = "REJECT"
        status = "Not Hired"

    return score, decision, status, matched, missing

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
if not st.session_state.logged_in:
    st.subheader("Recruiter Login")
    name = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.logged_in = True
        st.session_state.recruiter_name = name or "Recruiter"
        st.success("Login Successful")

# --------------------------------------------------
# ATS DASHBOARD
# --------------------------------------------------
else:
    st.success(f"Welcome {st.session_state.recruiter_name}")

    role = st.selectbox("Select Job Role", ROLE_SKILLS.keys())

    resumes = st.file_uploader(
        "Upload Candidate Resumes",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if st.button("Screen Resumes"):
        if not resumes:
            st.warning("Upload at least one resume")
        else:
            results = []
            for resume in resumes:
                if resume.type == "application/pdf":
                    text = read_pdf(resume)
                else:
                    text = resume.read().decode().lower()

                score, decision, status, matched, missing = evaluate_resume(text, role)

                results.append({
                    "Resume Name": resume.name,
                    "Role": role,
                    "AI Score (%)": score,
                    "Decision": decision,
                    "Hiring Status": status,
                    "Matched Skills": ", ".join(matched) if matched else "None",
                    "Missing Skills": ", ".join(missing) if missing else "None"
                })

            st.session_state.results_df = pd.DataFrame(results)

    # --------------------------------------------------
    # OUTPUT (ALWAYS VISIBLE)
    # --------------------------------------------------
    if st.session_state.results_df is not None:
        st.subheader("Screening Results")
        st.dataframe(st.session_state.results_df, use_container_width=True)

        buffer = BytesIO()
        st.session_state.results_df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            "Download Excel Report",
            buffer,
            "ATS_Results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.results_df = None
        st.success("Logged out")

