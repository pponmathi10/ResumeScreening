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
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

/* FULL PAGE BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0b132b, #0f2a44, #00f5d4);
    background-attachment: fixed;
    color: #eaeaea;
}

/* REMOVE EXTRA SPACE */
.block-container {
    padding-top: 1rem;
}

/* TITLE */
h1 {
    text-align: center;
    color: #00f5d4;
    text-shadow: 0 0 15px rgba(0,245,212,0.7);
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    color: #b8fff4;
    margin-bottom: 30px;
}

/* CARD STYLE */
.card {
    background: rgba(11,19,43,0.85);
    border: 1px solid rgba(0,245,212,0.4);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 25px;
    box-shadow: 0 0 20px rgba(0,245,212,0.25);
}

/* METRIC */
.metric {
    background: rgba(11,19,43,0.9);
    border: 1px solid #00f5d4;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}

/* DECISION */
.selected {
    color: #00f5d4;
    font-size: 22px;
    font-weight: bold;
}
.rejected {
    color: #ff5c5c;
    font-size: 22px;
    font-weight: bold;
}

/* SKILL TAG */
.skill {
    display: inline-block;
    padding: 7px 14px;
    margin: 6px;
    border-radius: 18px;
    background: rgba(0,245,212,0.15);
    border: 1px solid rgba(0,245,212,0.5);
}

/* IMPROVEMENT TIP */
.tip {
    border-left: 4px solid #00f5d4;
    padding: 12px;
    margin-bottom: 10px;
    background: rgba(11,19,43,0.8);
    border-radius: 10px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #00f5d4, #2ec4b6);
    color: #0b132b;
    font-weight: 600;
    padding: 12px 28px;
    border-radius: 12px;
    border: none;
    box-shadow: 0 0 15px rgba(0,245,212,0.6);
}
.stButton>button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)
# ==============================
# TITLE
# ==============================
st.markdown("<h1>NEON AI RESUME SCREENING</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-powered candidate evaluation</p>", unsafe_allow_html=True)

# ==============================
# ROLE SKILLS
# ==============================
ROLE_SKILLS = {
    "Java Developer": ["java", "spring", "sql", "oops"],
    "Python Developer": ["python", "django", "flask", "sql"],
    "Machine Learning Engineer": ["python", "machine learning", "pandas", "numpy"],
    "Web Developer": ["html", "css", "javascript", "react"]
}

# ==============================
# PDF READER
# ==============================
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for p in reader.pages:
        if p.extract_text():
            text += p.extract_text()
    return text.lower()

# ==============================
# INPUT
# ==============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
name = st.text_input("Candidate Name")
role = st.selectbox("Job Role", ROLE_SKILLS.keys())
resume = st.file_uploader("Upload Resume (PDF / TXT)", ["pdf", "txt"])
st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# SCREENING
# ==============================
if st.button("⚡ Screen Resume"):
    if not name or not resume:
        st.warning("Please upload resume")
        st.stop()

    text = read_pdf(resume) if resume.type == "application/pdf" else resume.read().decode().lower()
    skills = ROLE_SKILLS[role]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]
    score = int(len(matched) / len(skills) * 100)

    decision = "SELECTED" if score >= 50 else "REJECTED"

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Screening Result")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='metric'><h3>Match</h3><h1>{score}%</h1></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric'><h3>Status</h3><h1>{decision}</h1></div>", unsafe_allow_html=True)

    st.progress(score / 100)

    st.markdown("### Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill'>{s}</span>", unsafe_allow_html=True)

    st.markdown("### Improvements")
    for s in missing:
        st.markdown(f"<div class='tip'>Add experience in <b>{s}</b></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


