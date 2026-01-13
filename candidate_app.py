import streamlit as st
import PyPDF2

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="“Intelligent Resume Screening System Using NLP and Machine Learning”",
    layout="wide"
)

# ==================================================
# STRONG CONTRAST CSS (STREAMLIT CLOUD SAFE)
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* MAIN BACKGROUND */
.stApp {
    background-color: #0b1120;
    color: #e5e7eb;
}

/* HEADER */
.header {
    background: #020617;
    padding: 30px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 30px;
}

/* CARD */
.card {
    background: #020617;
    padding: 26px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 26px;
    color: #e5e7eb;
}

/* METRIC BOX */
.metric {
    background: #020617;
    border: 1px solid #475569;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    color: #f8fafc;
}

/* DECISION */
.selected {
    color: #22c55e;
    font-size: 22px;
    font-weight: 700;
}
.rejected {
    color: #ef4444;
    font-size: 22px;
    font-weight: 700;
}

/* SKILLS */
.skill {
    display: inline-block;
    background: #1e293b;
    color: #e0e7ff;
    padding: 6px 14px;
    margin: 6px;
    border-radius: 999px;
    border: 1px solid #475569;
    font-size: 14px;
}
.missing {
    background: #2a0f14;
    color: #fecaca;
    border-color: #991b1b;
}

/* IMPROVEMENT */
.tip {
    background: #020617;
    border-left: 5px solid #6366f1;
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #e5e7eb;
}

/* BUTTON */
.stButton>button {
    background: #6366f1;
    color: white;
    font-weight: 600;
    padding: 10px 28px;
    border-radius: 10px;
    border: none;
}
.stButton>button:hover {
    background: #4f46e5;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="header">
<h1>Executive AI Resume Screening</h1>
<p>Professional candidate evaluation system</p>
</div>
""", unsafe_allow_html=True)

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
# INPUT CARD
# ==================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Candidate Information")

name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
jd = st.text_area("Job Description (Optional)")
resume = st.file_uploader("Upload Resume (PDF / TXT)", ["pdf", "txt"])
st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# SCREEN
# ==================================================
if st.button("Run Resume Evaluation"):
    if not name or not resume:
        st.warning("Please enter candidate name and upload resume")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()
    score, decision, matched, missing, jd_score = evaluate(text, role, jd.lower() if jd else None)

    # ==================================================
    # OUTPUT CARD
    # ==================================================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Screening Result")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric'><h3>Skill Match</h3><h1>{score}%</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric'><h3>JD Match</h3><h1>{jd_score if jd_score else 'N/A'}%</h1></div>", unsafe_allow_html=True)

    st.progress(score / 100)

    status_class = "selected" if decision == "SELECTED" else "rejected"
    st.markdown(f"<p class='{status_class}'>Final Decision: {decision}</p>", unsafe_allow_html=True)

    st.markdown("### Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### Missing Skills")
        for s in missing:
            st.markdown(f"<span class='skill missing'>{s}</span>", unsafe_allow_html=True)

    st.markdown("### Improvement Recommendations")
    for s in missing:
        st.markdown(f"<div class='tip'>Improve <b>{s.title()}</b> with practical projects and certifications</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

