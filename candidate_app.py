import streamlit as st
import PyPDF2

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Resume Screening",
    layout="wide"
)

# ==================================================
# BLACK & WHITE PROFESSIONAL CSS
# ==================================================
st.markdown("""
<style>
/* GLOBAL */
.stApp {
    background-color: #ffffff;
    color: #000000;
    font-family: Arial, Helvetica, sans-serif;
}

/* HEADER */
.header {
    background-color: #000000;
    color: #ffffff;
    padding: 24px;
    border-radius: 8px;
    margin-bottom: 24px;
}

/* CARD */
.card {
    background-color: #ffffff;
    border: 2px solid #000000;
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
}

/* METRIC */
.metric-box {
    border: 2px solid #000000;
    padding: 20px;
    text-align: center;
    border-radius: 8px;
}

/* DECISION */
.selected {
    font-size: 20px;
    font-weight: bold;
}
.rejected {
    font-size: 20px;
    font-weight: bold;
}

/* SKILLS */
.skill {
    display: inline-block;
    border: 1px solid #000000;
    padding: 6px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 14px;
}

/* IMPROVEMENT */
.tip {
    border-left: 4px solid #000000;
    padding: 10px 14px;
    margin-bottom: 10px;
}

/* BUTTON */
.stButton>button {
    background-color: #000000;
    color: #ffffff;
    border-radius: 6px;
    padding: 10px 24px;
    font-weight: bold;
    border: none;
}
.stButton>button:hover {
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="header">
<h1>AI Resume Screening System</h1>
<p>Minimal & Professional Candidate Evaluation</p>
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
def evaluate_resume(text, role, jd=None):
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
if st.button("Screen Resume"):
    if not name or not resume:
        st.warning("Please enter candidate name and upload resume")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()
    score, decision, matched, missing, jd_score = evaluate_resume(text, role, jd.lower() if jd else None)

    # ==================================================
    # OUTPUT CARD
    # ==================================================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Screening Result")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric-box'><h3>Skill Match</h3><h2>{score}%</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-box'><h3>JD Match</h3><h2>{jd_score if jd_score else 'N/A'}%</h2></div>", unsafe_allow_html=True)

    st.progress(score / 100)

    st.markdown(f"<p class='selected'>Final Decision: {decision}</p>", unsafe_allow_html=True)

    st.markdown("### Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### Missing Skills")
        for s in missing:
            st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    st.markdown("### Improvement Suggestions")
    for s in missing:
        st.markdown(f"<div class='tip'>Improve knowledge in <b>{s.title()}</b></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
