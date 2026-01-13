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
# NEON CSS (PURPLE / PINK)
# ==============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Inter:wght@400;600&display=swap');

/* FULL PAGE BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #2b0033, #6a00ff, #ff00cc);
    background-attachment: fixed;
    color: white;
}

/* REMOVE EXTRA SPACE */
.block-container {
    padding-top: 1rem;
}

/* TITLE */
h1 {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    color: #ff00cc;
    text-shadow: 0 0 20px #ff00cc;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    margin-bottom: 30px;
    color: #ffe4ff;
}

/* CARD */
.card {
    background: rgba(0,0,0,0.6);
    border: 1px solid #ff00cc;
    border-radius: 18px;
    padding: 26px;
    margin-bottom: 30px;
    box-shadow: 0 0 25px #ff00cc;
}

/* METRIC */
.metric {
    background: rgba(0,0,0,0.7);
    border: 1px solid #ff00cc;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 15px #ff00cc;
}

/* DECISION */
.selected {
    color: #00ff9c;
    font-size: 22px;
    font-weight: bold;
}
.rejected {
    color: #ff4d4d;
    font-size: 22px;
    font-weight: bold;
}

/* SKILLS */
.skill {
    display: inline-block;
    padding: 8px 16px;
    margin: 6px;
    border-radius: 20px;
    background: rgba(255,0,204,0.2);
    border: 1px solid #ff00cc;
    box-shadow: 0 0 10px #ff00cc;
}

/* IMPROVEMENT */
.tip {
    border-left: 4px solid #ff00cc;
    padding: 14px;
    margin-bottom: 12px;
    background: rgba(0,0,0,0.6);
    border-radius: 10px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #ff00cc, #6a00ff);
    color: white;
    font-weight: bold;
    padding: 12px 32px;
    border-radius: 12px;
    border: none;
    box-shadow: 0 0 20px #ff00cc;
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
