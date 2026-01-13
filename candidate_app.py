import streamlit as st
import PyPDF2

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Neon AI Resume Screening",
    layout="wide"
)

# ==================================================
# NEON FULL BACKGROUND CSS
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Inter:wght@400;600&display=swap');

/* FULL BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #020024, #090979, #00d4ff);
    background-attachment: fixed;
    color: white;
}

/* REMOVE EXTRA TOP SPACE */
.block-container {
    padding-top: 1.5rem;
}

/* TITLE */
h1 {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    color: #00ffff;
    text-shadow: 0 0 15px #00ffff;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    color: #e0f7ff;
    margin-bottom: 30px;
}

/* CARD */
.card {
    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 26px;
    margin-bottom: 30px;
    border: 1px solid rgba(0, 255, 255, 0.4);
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.25);
}

/* METRIC */
.metric-box {
    background: rgba(0,0,0,0.6);
    border: 1px solid #00ffff;
    border-radius: 14px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 15px #00ffff;
}

/* DECISION */
.selected {
    color: #00ff9c;
    font-size: 22px;
    font-weight: 700;
    text-shadow: 0 0 10px #00ff9c;
}
.rejected {
    color: #ff4d4d;
    font-size: 22px;
    font-weight: 700;
    text-shadow: 0 0 10px #ff4d4d;
}

/* SKILLS */
.skill {
    display: inline-block;
    padding: 8px 16px;
    margin: 6px;
    border-radius: 999px;
    background: rgba(0,255,255,0.15);
    border: 1px solid #00ffff;
    color: #ffffff;
    box-shadow: 0 0 8px #00ffff;
}
.missing {
    border-color: #ff4d4d;
    box-shadow: 0 0 8px #ff4d4d;
}

/* IMPROVEMENT */
.tip {
    background: rgba(0,0,0,0.6);
    border-left: 4px solid #00ffff;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 0 10px rgba(0,255,255,0.4);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #00ffff, #00ff9c);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px 32px;
    border: none;
    box-shadow: 0 0 20px #00ffff;
}
.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# TITLE (NO EMPTY BOX BELOW)
# ==================================================
st.markdown("<h1>NEON AI RESUME SCREENING</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Next-generation resume evaluation powered by AI</p>", unsafe_allow_html=True)

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
# SCREENING
# ==================================================
if st.button("🚀 Run AI Screening"):
    if not name or not resume:
        st.warning("Please enter candidate name and upload resume")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()
    score, decision, matched, missing, jd_score = evaluate_resume(text, role, jd.lower() if jd else None)

    # ==================================================
    # OUTPUT
    # ==================================================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("AI Screening Result")

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

    st.markdown("### AI Improvement Suggestions")
    for s in missing:
        st.markdown(f"<div class='tip'>Enhance <b>{s.title()}</b> with real-time projects</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
