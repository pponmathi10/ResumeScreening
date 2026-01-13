import streamlit as st
import PyPDF2

# ==================================================
# ⚙️ PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Resume Screening Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 🎨 WEBSITE + INNOVATIVE UI CSS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

body {
    background: radial-gradient(circle at top, #0f2027, #000000);
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 60px;
    border-radius: 32px;
    color: white;
    box-shadow: 0 0 45px rgba(0,198,255,0.7);
    margin-bottom: 40px;
}
.hero h1 {
    font-size: 48px;
    font-weight: 800;
}
.hero p {
    font-size: 18px;
}

/* SECTION CARD */
.section-card {
    background: rgba(255,255,255,0.08);
    padding: 32px;
    border-radius: 26px;
    margin-bottom: 35px;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 30px rgba(255,255,255,0.15);
}

/* OUTPUT CONTAINER */
.output-container {
    background: linear-gradient(135deg,
        rgba(0,198,255,0.22),
        rgba(0,114,255,0.22)
    );
    border-radius: 30px;
    padding: 34px;
    margin-top: 30px;
    backdrop-filter: blur(18px);
    box-shadow: 0 0 40px rgba(0,198,255,0.5);
}

/* METRIC CARDS */
.metric-card {
    background: linear-gradient(145deg, #0f0f0f, #1e1e1e);
    border-radius: 22px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 25px rgba(0,255,171,0.35);
}

/* DECISION */
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

/* SKILLS */
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

/* IMPROVEMENT CARD */
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

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #00ffab, #00c6ff);
    color: black;
    font-weight: 700;
    border-radius: 20px;
    padding: 12px 30px;
    border: none;
    box-shadow: 0 0 18px rgba(0,255,171,0.6);
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #000000, #0f2027);
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 🌐 HERO SECTION (WEBPAGE FEEL)
# ==================================================
st.markdown("""
<div class="hero">
<h1>🤖 AI Resume Screening Platform</h1>
<p>
Smart candidate evaluation using role-based skill intelligence,
job description matching, and AI-powered improvement insights.
</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# 📌 SIDEBAR NAVIGATION
# ==================================================
st.sidebar.title("📌 Navigation")
st.sidebar.markdown("AI Resume Screening System")
st.sidebar.markdown("---")
st.sidebar.markdown("• Candidate Upload")
st.sidebar.markdown("• Skill Matching")
st.sidebar.markdown("• AI Evaluation")
st.sidebar.markdown("• Resume Improvement")
st.sidebar.markdown("---")
st.sidebar.success("🚀 Streamlit Cloud Ready")

# ==================================================
# 🧠 ROLE SKILLS
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
# 📄 PDF READER
# ==================================================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==================================================
# 📊 EVALUATION LOGIC
# ==================================================
def evaluate_resume(text, role, jd=None):
    skills = ROLE_SKILLS[role]["skills"]
    main = ROLE_SKILLS[role]["main"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]

    score = int(len(matched) / len(skills) * 100)

    decision = "SELECTED" if (
        main in text or len(matched) >= 2 or score >= 50
    ) else "REJECTED"

    jd_score = None
    if jd:
        jd_words = [w for w in jd.split() if len(w) > 3]
        jd_match = [w for w in jd_words if w in text]
        jd_score = int(len(jd_match) / max(len(jd_words), 1) * 100)

    return score, decision, matched, missing, jd_score

# ==================================================
# 🚀 IMPROVEMENT ENGINE
# ==================================================
def improvements(role, missing):
    tips = []
    for s in missing:
        tips.append({
            "skill": s,
            "priority": "High" if s in ROLE_SKILLS[role]["skills"][:3] else "Medium",
            "action": f"Add {s.title()} with real-time project & GitHub link"
        })

    project_map = {
        "Java Developer": "Spring Boot REST API with MySQL",
        "Python Developer": "Django Full Stack App",
        "Machine Learning Engineer": "ML Model + Deployment",
        "Data Scientist": "EDA + Prediction System",
        "Web Developer": "Responsive React Portfolio"
    }
    return tips, project_map.get(role)

# ==================================================
# 🧑 INPUT SECTION
# ==================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("📤 Candidate Resume Upload")

name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
jd = st.text_area("Job Description (Optional)")
resume = st.file_uploader("Upload Resume (PDF/TXT)", ["pdf", "txt"])

st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# 🚀 SCREEN BUTTON
# ==================================================
if st.button("🚀 Screen Resume"):
    if not name or not resume:
        st.warning("Please enter name and upload resume")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()

    score, decision, matched, missing, jd_score = evaluate_resume(
        text, role, jd.lower() if jd else None
    )

    tips, project = improvements(role, missing)

    # ==================================================
    # 📊 OUTPUT SECTION (INNOVATIVE)
    # ==================================================
    st.markdown('<div class="output-container">', unsafe_allow_html=True)
    st.markdown("## 📊 AI Screening Result")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric-card'><h3>Skill Match</h3><h1>{score}%</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h3>JD Match</h3><h1>{jd_score if jd_score else 'N/A'}%</h1></div>", unsafe_allow_html=True)

    st.progress(score / 100)

    cls = "selected" if decision == "SELECTED" else "rejected"
    st.markdown(f"<p class='{cls}'>Final Decision: {decision}</p>", unsafe_allow_html=True)

    st.markdown("### ✅ Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### ❌ Missing Skills")
        for s in missing:
            st.markdown(f"<span class='skill missing'>{s}</span>", unsafe_allow_html=True)

    st.markdown("## 🚀 AI-Based Improvements")
    for t in tips:
        st.markdown(f"""
        <div class="improve-card">
        🔧 <b>{t['skill'].title()}</b><br>
        👉 {t['action']}<br>
        ⚡ Priority: <b>{t['priority']}</b>
        </div>
        """, unsafe_allow_html=True)

    if project:
        st.markdown(f"""
        <div class="improve-card">
        📌 <b>Recommended Project</b><br>
        Build: <b>{project}</b><br>
        Add GitHub & Deployment link
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

