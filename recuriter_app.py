import streamlit as st
import PyPDF2
import pandas as pd
from io import BytesIO

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(page_title="Recruiter ATS Resume Screening", layout="wide")
st.title("🧑‍💼 Recruiter ATS Resume Screening")
st.caption("Signup | Login | Bulk Resume Screening | Excel Export")

# --------------------------------------------------
# Session State Initialization
# --------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {}   # stores username:password

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# --------------------------------------------------
# Job Roles & Skills
# --------------------------------------------------
ROLE_SKILLS = {
    "Java Developer": {
        "main": "java",
        "skills": ["java", "spring", "sql", "oops", "data structures"]
    },
    "Python Developer": {
        "main": "python",
        "skills": ["python", "django", "flask", "sql", "oops"]
    },
    "Machine Learning Engineer": {
        "main": "machine learning",
        "skills": ["python", "machine learning", "pandas", "numpy", "scikit-learn"]
    }
}

# --------------------------------------------------
# PDF Reader
# --------------------------------------------------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# --------------------------------------------------
# Resume Evaluation Logic
# --------------------------------------------------
def evaluate_resume(text, role):
    main_skill = ROLE_SKILLS[role]["main"]
    skills = ROLE_SKILLS[role]["skills"]

    matched = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]

    score = int((len(matched) / len(skills)) * 100)

    if (main_skill in text) or (len(matched) >= 2) or (score >= 50):
        decision = "SELECT"
        hiring_status = "Hired"
    else:
        decision = "REJECT"
        hiring_status = "Not Hired"

    return score, decision, hiring_status, matched, missing, skills

# ==================================================
# 🔐 SIGNUP & LOGIN
# ==================================================
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["📝 Signup", "🔐 Login"])

    # ---------- SIGNUP ----------
    with tab1:
        st.subheader("Create Recruiter Account")

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Signup"):
            if not new_user or not new_pass:
                st.warning("Please fill all fields")
            elif new_user in st.session_state.users:
                st.error("Username already exists")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account created successfully! Please login.")

    # ---------- LOGIN ----------
    with tab2:
        st.subheader("Recruiter Login")

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):
            if user in st.session_state.users and st.session_state.users[user] == pwd:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.success("Login successful")
            else:
                st.error("Invalid username or password")

# ==================================================
# 📊 ATS DASHBOARD (AFTER LOGIN)
# ==================================================
else:
    st.success(f"Logged in as: {st.session_state.current_user}")

    role = st.selectbox("Select Job Role", ROLE_SKILLS.keys())

    resumes = st.file_uploader(
        "Upload Candidate Resumes (Multiple files allowed)",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if st.button("🔍 Screen All Resumes"):
        if not resumes:
            st.warning("Please upload at least one resume")
        else:
            results = []

            for resume in resumes:
                if resume.type == "application/pdf":
                    text = read_pdf(resume)
                else:
                    text = resume.read().decode("utf-8").lower()

                score, decision, hiring_status, matched, missing, skills = evaluate_resume(
                    text, role
                )

                results.append({
                    "Resume File": resume.name,
                    "Job Role": role,
                    "AI Score (%)": score,
                    "Decision": decision,
                    "Hiring Status": hiring_status,
                    "Matched Skills": ", ".join(matched) if matched else "None",
                    "Missing Skills": ", ".join(missing) if missing else "None"
                })

            df = pd.DataFrame(results)

            st.subheader("📋 Resume Screening Results")
            st.dataframe(df, use_container_width=True)

            # -------- Excel Download --------
            buffer = BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)

            st.download_button(
                label="⬇️ Download Results as Excel",
                data=buffer,
                file_name="ATS_Resume_Screening_Results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # ---------- LOGOUT ----------
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.success("Logged out successfully")
