import streamlit as st
import PyPDF2

# ==================================================
# ⚙️ Page Configuration
# ==================================================
st.set_page_config(page_title="Candidate Resume Screening", layout="wide")

# ==================================================
# 🎨 Custom UI Styling (Streamlit Cloud Friendly)
# ==================================================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main {
    background: rgba(255,255,255,0.04);
}
.card {
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}
.skill {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px;
    border-radius: 12px;
    background: #00c6ff;
    color: black;
    font-weight: 600;
}
.missing {
    background: #ff6b6b;
    color: white;
}
.selected {
    color: #00ffab;
    font-size: 24px;
    font-weight: bold;
}
.rejected {
    color: #ff4b4b;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 🏷️ App Title
# ==================================================
st.title("🧑 Candidate Resume Screening Portal")
st.caption("AI-based Resume Evaluation (JD Optional)")

# ==================================================
# 🧠 Job Roles & Required Skills
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
# 🚀 Resume Improvement Engine
# ==================================================
def improvement_suggestions(role, missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append({
            "skill": skill,
            "action": f"Learn and add **{skill.title()}** with a mini project",
            "priority": "High" if skill in ROLE_SKILLS[role]["skills"][:3] else "Medium"
        })

    role_projects = {
        "Java Developer": "Spring Boot REST API with MySQL",
        "Python Developer": "Django CRUD Application",
        "Machine Learning Engineer": "End-to-End ML Model with Deployment",
        "Data Scientist": "EDA + ML on Real Kaggle Dataset",
        "Web Developer": "Responsive React Portfolio Website"
    }

    return suggestions, role_projects.get(role)

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

# ==================================================
# 🚀 Screening Button
# ==================================================
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
    # 📊 Screening Result
    # ==================================================
    st.markdown("## 📊 Screening Result")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("Resume Skill Match", f"{score}%")
    col2.metric("JD Match Score", f"{jd_score}%" if jd_score is not None else "Not Provided")
    st.progress(score / 100)
    st.markdown('</div>', unsafe_allow_html=True)

    decision_class = "selected" if decision == "SELECTED" else "rejected"
    st.markdown(
        f"<div class='{decision_class}'>Final Decision: {decision}</div>",
        unsafe_allow_html=True
    )

    # ==================================================
    # ✅ Skill Visualization
    # ==================================================
    st.markdown("### ✅ Matched Skills")
    for skill in matched:
        st.markdown(f"<span class='skill'>{skill}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### ❌ Missing Skills")
        for skill in missing:
            st.markdown(f"<span class='skill missing'>{skill}</span>", unsafe_allow_html=True)

    # ==================================================
    # 🚀 Resume Improvement Suggestions
    # ==================================================
    st.markdown("## 🚀 Things to Improve (Based on Your Resume)")

    suggestions, project = improvement_suggestions(role, missing)

    if suggestions:
        for s in suggestions:
            st.markdown(f"""
            <div class="card">
            🔧 <b>{s['skill'].title()}</b><br>
            👉 {s['action']}<br>
            ⚡ Priority: <b>{s['priority']}</b>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("Excellent! Your resume covers all required skills 🎯")

    if project:
        st.markdown(f"""
        <div class="card">
        📌 <b>Recommended Project for {role}</b><br>
        Build: <b>{project}</b><br>
        Add GitHub + Deployment link in resume
        </div>
        """, unsafe_allow_html=True)


