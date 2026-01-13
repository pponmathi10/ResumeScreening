import streamlit as st
import PyPDF2

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    layout="wide"
)

# ==================================================
# AI SAAS UI – GLASSMORPHISM CSS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(120deg, #f8fafc, #eef2ff);
}

/* HEADER */
.ai-header {
    background: linear-gradient(135deg, #6366f1, #3b82f6);
    padding: 36px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
}

/* GLASS CARD */
.glass {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 28px;
}

/* METRIC */
.metric-box {
    background: white;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

/* DECISION */
.selected {
    color: #16a34a;
    font-weight: 700;
    font-size: 22px;
}
.rejected {
    color: #dc2626;
    font-weight: 700;
    font-size: 22px;
}

/* SKILLS */
.skill {
    display: inline-block;
    padding: 8px 16px;
    margin: 6px;
    border-radius: 999px;
    background: #eef2ff;
    color: #4338ca;
    font-size: 14px;
}
.missing {
    background: #fee2e2;
    color: #991b1b;
}

/* AI INSIGHT */
.ai-tip {
    background: linear-gradient(90deg, #eef2ff, #f8fafc);
    border-left: 5px solid #6366f1;
    padding: 14px 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #3b82f6);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 12px 30px;
    border: none;
}
.stButton>button:hover {
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="ai-header">
<h1>AI Resume Intelligence Platform</h1>
<p>Smart resume evaluation powered by Artificial Intelligence</p>
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
# EVALUATION LOGIC
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
# INPUT – GLASS CARD
# ==================================================
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("Candidate Resume Submission")

name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
jd = st.text_area("Job Description (Optional)")
resume = st.file_uploader("Upload Resume (PDF / TXT)", ["pdf", "txt"])

st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# RUN AI SCREENING
# ==================================================
if st.button("Run AI Resume Analysis"):
    if not name or not resume:
        st.warning("Please enter candidate name and upload resume")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()
    score, decision, matched, missing, jd_score = evaluate_resume(text, role, jd.lower() if jd else None)

    # ==================================================
    # OUTPUT – AI INSIGHTS
    # ==================================================
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.subheader("AI Evaluation Result")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric-box'><h3>Skill Match</h3><h1>{score}%</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-box'><h3>JD Match</h3><h1>{jd_score if jd_score else 'N/A'}%</h1></div>", unsafe_allow_html=True)

    st.progress(score / 100)

    status = "selected" if decision == "SELECTED" else "rejected"
    st.markdown(f"<p class='{status}'>Final Decision: {decision}</p>", unsafe_allow_html=True)

    st.markdown("### Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    if missing:
        st.markdown("### Missing Skills")
        for s in missing:
            st.markdown(f"<span class='skill missing'>{s}</span>", unsafe_allow_html=True)

    st.markdown("### AI Improvement Insights")
    for s in missing:
        st.markdown(
            f"<div class='ai-tip'>AI suggests strengthening <b>{s.title()}</b> with hands-on projects and certifications</div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
