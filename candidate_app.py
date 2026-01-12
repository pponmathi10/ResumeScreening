import streamlit as st
import PyPDF2

st.set_page_config(page_title="Candidate Resume Screening", layout="wide")

st.title("🧑 Candidate Resume Screening Portal")
st.caption("AI-based Resume Evaluation (JD Optional)")

# ==================================================
# 🧠 Job Roles, Main Skill & Required Skills
# ==================================================
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "spring boot", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "scikit-learn", "pandas", "numpy"]
    },
    "Data Scientist": {
        "main": "python",
        "skills": ["python", "machine learning", "statistics", "pandas", "sql"]
    },
    "Web Developer": {
        "main": "javascript",
        "skills": ["html", "css", "javascript", "react", "bootstrap"]
    }
}

# ==================================================
# 📄 PDF Reader
# ==================================================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==================================================
# 📊 Resume Evaluation Logic
# ==================================================
def evaluate_resume(resume_text, role, jd_text=None):
    role_data = ROLE_SKILLS[role]
    main_skill = role_data["main"]
    required_skills = role_data["skills"]

    matched = [s for s in required_skills if s in resume_text]
    missing = [s for s in required_skills if s not in resume_text]

    score = int((len(matched) / len(required_skills)) * 100)

    main_skill_present = main_skill in resume_text
    two_skills_present = len(matched) >= 2
    percentage_pass = score >= 50

    decision = "SELECTED" if (
        main_skill_present or two_skills_present or percentage_pass
    ) else "REJECTED"

    # JD Matching (Optional)
    jd_score = None
    if jd_text:
        jd_words = [w for w in jd_text.split() if len(w) > 3]
        jd_matched = [w for w in jd_words if w in resume_text]
        jd_score = int((len(jd_matched) / max(len(jd_words), 1)) * 100)

    return score, decision, matched, missing, main_skill_present, jd_score

# ==================================================
# 🧑 Candidate Input
# ==================================================
st.subheader("📤 Upload Your Resume")

candidate_name = st.text_input("Candidate Name")
role = st.selectbox("Job Role Applying For", ROLE_SKILLS.keys())

job_description = st.text_area(
    "Job Description (Optional)",
    placeholder="Paste the job description here (optional)"
)

resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"])

if st.button("🚀 Screen My Resume"):
    if not candidate_name or not resume_file:
        st.warning("Please enter your name and upload your resume")
        st.stop()

    resume_text = (
        read_pdf(resume_file)
        if resume_file.type == "application/pdf"
        else resume_file.read().decode("utf-8").lower()
    )

    jd_text = job_description.lower() if job_description else None

    score, decision, matched, missing, main_skill_present, jd_score = evaluate_resume(
        resume_text, role, jd_text
    )

    # ==================================================
    # 📊 Output
    # ==================================================
    st.markdown("## 📊 Screening Result")

    col1, col2 = st.columns(2)
    col1.metric("Resume Skill Match", f"{score}%")
    col2.metric("JD Match Score", f"{jd_score}%" if jd_score is not None else "Not Provided")

    st.progress(score / 100)
    st.markdown(f"### 🧾 Final Decision: **{decision}**")

    # ==================================================
    # ✅ SELECTED OUTPUT
    # ==================================================
    if decision == "SELECTED":
        st.success("🎉 Congratulations! Your resume meets the selection criteria.")

        st.info("✅ Strengths Identified")
        st.write("Matched Skills:", ", ".join(matched))

        st.markdown("### 📈 How You Can Improve Further")
        st.write(
            "- Add **real-time projects** related to your role\n"
            "- Include **certifications** for missing or advanced skills\n"
            "- Mention **tools & frameworks** clearly\n"
            "- Quantify achievements (e.g., improved performance by 20%)"
        )

        if missing:
            st.warning("💡 Optional Skills to Learn:")
            st.write(", ".join(missing))

    # ==================================================
    # ❌ REJECTED OUTPUT
    # ==================================================
    else:
        st.error("❌ Your resume does not meet the minimum criteria.")

        st.markdown("### 🔧 Skills You Need to Improve")
        st.warning(", ".join(missing))

        st.markdown("### 📝 Resume Improvement Suggestions")
        st.write(
            "- Add **main skill** prominently in summary and skills section\n"
            "- Include **hands-on projects** using missing skills\n"
            "- Use **job description keywords** in resume\n"
            "- Improve resume formatting for ATS (simple, clean layout)\n"
            "- Add internships, workshops, or certifications"
)

