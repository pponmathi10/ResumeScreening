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
import streamlit as st
import PyPDF2

# ==================================================
# ⚙️ Page Configuration
# ==================================================
st.set_page_config(page_title="AI Resume Screening", layout="wide")

# ==================================================
# 🎨 ADVANCED INNOVATIVE UI (NOT SIMPLE)
# ==================================================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #000000);
}

/* Output Glass Container */
.output-container {
    background: linear-gradient(
        135deg,
        rgba(0, 198, 255, 0.20),
        rgba(0, 114, 255, 0.20)
    );
    border-radius: 26px;
    padding: 32px;
    margin-top: 25px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 0 35px rgba(0, 198, 255, 0.45);
    border: 1px solid rgba(255,255,255,0.2);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(145deg, #0f0f0f, #1f1f1f);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 25px rgba(0,255,171,0.35);
}

/* Decision Glow */
.selected {
    color: #00ffab;
    font-size: 28px;
    font-weight: 900;
    text-shadow: 0 0 18px #00ffab;
}
.rejected {
    color: #ff4b4b;
    font-size: 28px;
    font-weight: 900;
    text-shadow: 0 0 18px #ff4b4b;
}

/* Skill Badges */
.skill {
    display: inline-block;
    padding: 8px 16px;
    margin: 6px;
    border-radius: 22px;
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    font-weight: 700;
    box-shadow: 0 0 14px rgba(0,198,255,0.7);
}
.missing {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    box-shadow: 0 0 14px rgba(255,75,75,0.8);
}

/* Improvement Cards */
.improve-card {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.12),
        rgba(255,255,255,0.05)
    );
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 0 22px rgba(255,255,255,0.15);
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 🏷️ App Title
# ==================================================
st.title("🧑‍💼 AI Candidate Resume Screening Portal")
st.caption("Smart Resume Evaluation with Skill Intelligence")

# ==================================================
# 🧠 Job Roles & Skills
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
# 📊 Resume Evaluation
# ==================================================
def evaluate_resume(resume_text, role, jd_text=None):
    data = ROLE_SKILLS[role]
    required_skills = data["skills"]
    main_skill = data["main"]

    matched = [s for s in required_skills if s in resume_text]
    missing = [s for s in required_skills if s not in resume_text]

    score = int((len(matched) / len(required_skills)) * 100)

    decision = "SELECTED" if (
        main_skill in resume_text or len(matched) >= 2 or score >= 50
    ) else "REJECTED"

    jd_score = None
    if jd_text:
        jd_words = [w for w in jd_text.split() if len(w) > 3]
        jd_match = [w for w in jd_words if w in resume_text]
        jd_score = int((len(jd_match) / max(len(jd_words), 1)) * 100)

    return score, decision, matched, missing, jd_score

# ==================================================
# 🚀 Improvement Engine
# ==================================================
def improvement_suggestions(role, missing):
    suggestions = []
    for skill in missing:
        suggestions.append({
            "skill": skill,
            "action": f"Add **{skill.title()}** with hands-on project & GitHub link",
            "priority": "High" if skill in ROLE_SKILLS[role]["skills"][:3] else "Medium"
        })

    projects = {
        "Java Developer": "Spring Boot REST API + MySQL",
        "Python Developer": "Django Full Stack App",
        "Machine Learning Engineer": "ML Model with Deployment",
        "Data Scientist": "EDA + Prediction on Kaggle Data",
        "Web Developer": "Responsive React Portfolio"
    }
    return suggestions, projects.get(role)

# ==================================================
# 🧑 Candidate Input
# ==================================================
st.subheader("📤 Upload Resume")

name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
jd = st.text_area("Job Description (Optional)")
resume = st.file_uploader("Upload Resume (PDF/TXT)", ["pdf", "txt"])

# ==================================================
# 🚀 Run Screening
# ==================================================
if st.button("🚀 Screen Resume"):
    if not name or not resume:
        st.warning("Please enter name and upload resume")
        st.stop()

    resume_text = (
        read_pdf(resume)
        if resume.type == "application/pdf"
        else resume.read().decode("utf-8").lower()
    )

    score, decision, matched, missing, jd_score = evaluate_resume(
        resume_text, role, jd.lower() if jd else None
    )

    suggestions, project = improvement_suggestions(role, missing)

    # ==================================================
    # 📊 OUTPUT (INNOVATIVE)
    # ==================================================
    st.markdown('<div class="output-container">', unsafe_allow_html=True)
    st.markdown("## 📊 AI Resume Screening Result")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Skill Match</h3>
        <h1>{score}%</h1>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>JD Match</h3>
        <h1>{jd_score if jd_score is not None else 'N/A'}%</h1>
        </div>
        """, unsafe_allow_html=True)

    st.progress(score / 100)

    decision_class = "selected" if decision == "SELECTED" else "rejected"
    st.markdown(f"<p class='{decision_class}'>Final Decision: {decision}</p>", unsafe_allow_html=True)

    st.markdown("### ✅ Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### ❌ Missing Skills")
        for s in missing:
            st.markdown(f"<span class='skill missing'>{s}</span>", unsafe_allow_html=True)

    st.markdown("## 🚀 AI-Based Resume Improvements")
    for s in suggestions:
        st.markdown(f"""
        <div class="improve-card">
        🔧 <b>{s['skill'].title()}</b><br>
        👉 {s['action']}<br>
        ⚡ Priority: <b>{s['priority']}</b>
        </div>
        """, unsafe_allow_html=True)

    if project:
        st.markdown(f"""
        <div class="improve-card">
        📌 <b>Recommended Project</b><br>
        Build: <b>{project}</b><br>
        Add GitHub + Deployment URL
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
