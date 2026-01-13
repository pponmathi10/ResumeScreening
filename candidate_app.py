import streamlit as st
import PyPDF2

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Enterprise AI Resume Screening",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# PROFESSIONAL ENTERPRISE UI CSS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* MAIN BACKGROUND */
body {
    background: linear-gradient(180deg, #f4f7fb, #e9eef5);
}

/* HEADER */
.header {
    background: linear-gradient(90deg, #1f3c88, #2f5bea);
    padding: 35px;
    border-radius: 16px;
    color: white;
    margin-bottom: 30px;
}

/* SECTION */
.section {
    background: white;
    padding: 28px;
    border-radius: 14px;
    margin-bottom: 30px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.06);
}

/* OUTPUT CONTAINER */
.output {
    background: linear-gradient(180deg, #ffffff, #f6f9fc);
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.08);
    margin-top: 30px;
}

/* METRIC BOX */
.metric {
    background: #f4f7fb;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border-left: 6px solid #2f5bea;
}

/* DECISION */
.selected {
    color: #1a7f37;
    font-size: 24px;
    font-weight: 700;
}
.rejected {
    color: #b42318;
    font-size: 24px;
    font-weight: 700;
}

/* SKILLS */
.skill {
    display: inline-block;
    padding: 6px 14px;
    margin: 6px;
    border-radius: 20px;
    background: #e6edff;
    color: #1f3c88;
    font-weight: 600;
}
.missing {
    background: #fdecea;
    color: #b42318;
}

/* IMPROVEMENT */
.improve {
    background: #f9fafb;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 14px;
    border-left: 4px solid #2f5bea;
}

/* BUTTON */
.stButton>button {
    background: #2f5bea;
    color: white;
    font-weight: 600;
    padding: 10px 26px;
    border-radius: 10px;
    border: none;
}
.stButton>button:hover {
    background: #1f3c88;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER (ENTERPRISE STYLE)
# ==================================================
st.markdown("""
<div class="header">
<h1>AI Resume Screening System</h1>
<p>Enterprise-grade candidate evaluation and skill intelligence platform</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("HR Navigation")
st.sidebar.markdown("• Resume Screening")
st.sidebar.markdown("• Skill Evaluation")
st.sidebar.markdown("• Candidate Insights")
st.sidebar.markdown("• Hiring Recommendation")

# ==================================================
# ROLE SKILLS
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
# PDF READER
# ==================================================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==================================================
# EVALUATION
# ==================================================
def evaluate(text, role, jd=None):
    skills = ROLE_SKILLS[role]["skills"]
    main = ROLE_SKILLS[role]["main"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]
    score = int(len(matched) / len(skills) * 100)

    decision = "SELECTED" if (
        main in text or score >= 50 or len(matched) >= 2
    ) else "REJECTED"

    jd_score = None
    if jd:
        words = [w for w in jd.split() if len(w) > 3]
        match = [w for w in words if w in text]
        jd_score = int(len(match) / max(len(words), 1) * 100)

    return score, decision, matched, missing, jd_score

# ==================================================
# IMPROVEMENTS
# ==================================================
def improvements(role, missing):
    tips = []
    for s in missing:
        tips.append(f"Add hands-on experience in {s.title()} with a project")

    projects = {
        "Java Developer": "Spring Boot REST API",
        "Python Developer": "Django CRUD Application",
        "Machine Learning Engineer": "ML Model with Deployment",
        "Data Scientist": "EDA + ML Pipeline",
        "Web Developer": "Responsive Web Portfolio"
    }
    return tips, projects.get(role)

# ==================================================
# INPUT SECTION
# ==================================================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("Candidate Resume Upload")

name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
jd = st.text_area("Job Description (Optional)")
resume = st.file_uploader("Upload Resume (PDF/TXT)", ["pdf", "txt"])
st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# SCREENING
# ==================================================
if st.button("Evaluate Resume"):
    if not name or not resume:
        st.warning("Please upload resume and enter candidate name")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()
    score, decision, matched, missing, jd_score = evaluate(text, role, jd.lower() if jd else None)
    tips, project = improvements(role, missing)

    # ==================================================
    # OUTPUT
    # ==================================================
    st.markdown('<div class="output">', unsafe_allow_html=True)
    st.subheader("Screening Results")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric'><h3>Skill Match</h3><h2>{score}%</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric'><h3>JD Match</h3><h2>{jd_score if jd_score else 'N/A'}%</h2></div>", unsafe_allow_html=True)

    st.progress(score / 100)

    cls = "selected" if decision == "SELECTED" else "rejected"
    st.markdown(f"<p class='{cls}'>Final Decision: {decision}</p>", unsafe_allow_html=True)

    st.markdown("### Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### Missing Skills")
        for s in missing:
            st.markdown(f"<span class='skill missing'>{s}</span>", unsafe_allow_html=True)

    st.markdown("### Resume Improvement Suggestions")
    for t in tips:
        st.markdown(f"<div class='improve'>• {t}</div>", unsafe_allow_html=True)

    if project:
        st.markdown(f"<div class='improve'><b>Recommended Project:</b> {project}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


