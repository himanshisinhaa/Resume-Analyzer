# app.py
import streamlit as st
from analyzer import extract_text, compute_match_score, extract_skills, build_suggestions, generate_pdf_report_bytes

st.set_page_config(page_title="Resume Analyzer (Recruiter)", layout="wide", page_icon="📄")

st.markdown("<center><h1>📄 AI Resume Analyzer — Recruiter View</h1></center>", unsafe_allow_html=True)
st.write("Upload a resume and paste the job description.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Upload")
    resume_file = st.file_uploader("📄 Upload Resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])
    jd_text = st.text_area("📑 Paste Job Description here", height=240)
    analyze = st.button("🔎 Analyze Resume")

with col2:
    st.subheader("Results")
    placeholder = st.empty()

if analyze:
    if not resume_file or not jd_text.strip():
        st.warning("Please upload a resume and paste the job description before analyzing.")
    else:
        with st.spinner("Analyzing — embeddings + skill check (few seconds)..."):
            resume_text = extract_text(resume_file)
            score = compute_match_score(resume_text, jd_text)
            found, missing = extract_skills(resume_text)
            note, rec_lines = build_suggestions(found, missing, score)

        st.metric("Overall Match Score", f"{score}%")
        st.progress(score/100)

        left, right = st.columns(2)
        with left:
            st.subheader("✅ Skills Found")
            st.write(", ".join(found) if found else "No skills from the list were found.")
        with right:
            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing) if missing else "No major missing skills from the list.")

        st.subheader("📌 Recruiter Notes")
        st.info(note)
        for r in rec_lines:
            st.write("-", r)

        # generate PDF report
        pdf_bytes = generate_pdf_report_bytes(score, found, missing, rec_lines, resume_name=resume_file.name)
        st.download_button("📥 Download Report (PDF)", data=pdf_bytes, file_name="resume_report.pdf", mime="application/pdf")
