import streamlit as st
import PyPDF2
import pandas as pd
from io import BytesIO

# ---------------- Page Config ----------------
st.set_page_config(page_title="Recruiter ATS Resume Screening", layout="wide")

st.title("🧑‍💼 Recruiter ATS Resume Screening")
st.caption("Bulk Resume Screening with AI Score & Hiring Decision")

# ---------------- Job Roles & Skills ----------------
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

# ---------------- PDF Reader ----------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text.lower()

# ---------------- Resume Evaluation Logic ----------------
def evaluate_resume(text, role):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]

    score = int((len(matched) / len(skills)) * 100)

    # Selection Conditions
    if (main_skill in text) or (len(matched) >= 2) or (score >= 50):
        decision = "SELECT"
        hiring_status = "Hired"
    else:
        decision = "REJECT"
        hiring_status = "Not Hired"

    return score, decision, hiring_status, matched, missing, skills

# ---------------- UI ----------------
role = st.selectbox("Select Job Role", ROLE_SKILLS.keys())

resumes = st.file_uploader(
    "Upload Candidate Resumes (Multiple Files Allowed)",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if st.button("🔍 Screen All Resumes"):
    if not resumes:
        st.warning("Please upload at least one resume")
    else:
        results = []

        for resume in resumes:
            if resume.type == "application/pdf":
                resume_text = read_pdf(resume)
            else:
                resume_text = resume.read().decode("utf-8").lower()

            score, decision, hiring_status, matched, missing, skills = evaluate_resume(
                resume_text, role
            )

            results.append({
                "Resume File": resume.name,
                "Job Role": role,
                "AI Score (%)": score,
                "Decision": decision,
                "Hiring Status": hiring_status,
                "Matched Skills": ", ".join(matched) if matched else "None",
                "Missing Skills": ", ".join(missing) if missing else "None"
            })

        df = pd.DataFrame(results)

        st.subheader("📋 Resume Screening Results")
        st.dataframe(df, use_container_width=True)

        # ---------------- Excel Download ----------------
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Results as Excel",
            data=excel_buffer,
            file_name="ATS_Resume_Screening_Results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
