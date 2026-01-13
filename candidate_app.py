import streamlit as st
import PyPDF2

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Resume Screening",
    layout="wide"
)

# ==============================
# CSS (Clean Dark + Teal Neon accents)
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #0b132b, #1c2541, #00b4d8);
    background-attachment: fixed;
    color: #eaeaea;
}
.block-container { padding-top: 1rem; }

h1 { text-align: center; color: #ffffff; font-weight: 600; letter-spacing: 1px; text-shadow: none; }
.subtitle { text-align: center; color: #cbd5e1; margin-bottom: 30px; }

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

.selected { color: #00ff9c; font-size: 22px; font-weight: 600; }
.rejected { color: #ff6b6b; font-size: 22px; font-weight: 600; }

.skill {
    display: inline-block; padding: 7px 14px; margin: 6px;
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

# ==============================
# TITLE
# ==============================
st.markdown("<h1>AI Resume Screening System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Automated Candidate Evaluation Platform</p>", unsafe_allow_html=True)

# ==============================
# ROLE SKILLS
# ==============================
ROLE_SKILLS = {
    "Java Developer": {"main": "java", "skills": ["java", "spring", "spring boot", "sql", "oops", "data structures"]},
    "Python Developer": {"main": "python", "skills": ["python", "django", "flask", "sql", "oops"]},
    "Machine Learning Engineer": {"main": "machine learning", "skills": ["python", "machine learning", "scikit-learn", "pandas", "numpy"]},
    "Data Scientist": {"main": "python", "skills": ["python", "machine learning", "statistics", "pandas", "sql"]},
    "Web Developer": {"main": "javascript", "skills": ["html", "css", "javascript", "react", "bootstrap"]}
}

# ==============================
# PDF READER
# ==============================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ==============================
# RESUME EVALUATION
# ==============================
def evaluate_resume(text, role, jd=None):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]

    score = int(len(matched) / len(skills) * 100)

    # DECISION LOGIC: MAIN SKILL OR ≥50%
    decision = "SELECTED" if (main_skill in text or score >= 50) else "REJECTED"

    # JD MATCH
    jd_score = None
    if jd:
        jd_words = [w.lower() for w in jd.split() if len(w) > 3]
        jd_matched = [w for w in jd_words if w in text]
        jd_score = int(len(jd_matched) / max(len(jd_words), 1) * 100)

    return score, decision, matched, missing, jd_score

# ==============================
# INPUT CARD
# ==============================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Candidate Information")
name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
jd = st.text_area("Job Description (Optional)")
resume = st.file_uploader("Upload Resume (PDF / TXT)", ["pdf", "txt"])
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# SCREENING
# ==============================
if st.button("⚡ Screen Resume"):
    if not name or not resume:
        st.warning("Please enter candidate name and upload resume")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()
    score, decision, matched, missing, jd_score = evaluate_resume(text, role, jd.lower() if jd else None)

    # ==============================
    # OUTPUT CARD
    # ==============================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Screening Result")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric'><h3>Skill Match</h3><h1>{score}%</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric'><h3>JD Match</h3><h1>{jd_score if jd_score is not None else 'N/A'}%</h1></div>", unsafe_allow_html=True)

    st.progress(score / 100)

    status_class = "selected" if decision == "SELECTED" else "rejected"
    st.markdown(f"<p class='{status_class}'>Final Decision: {decision}</p>", unsafe_allow_html=True)

    st.markdown("### Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### Missing Skills / Improvements")
        for s in missing:
            st.markdown(f"<div class='tip'>Improve knowledge in <b>{s}</b> or add projects/certifications</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
