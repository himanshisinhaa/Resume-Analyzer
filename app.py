# import streamlit as st
# import requests

# st.title("AI-Powered Resume Analyzer")

# uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
# if uploaded_file:
#     files = {"file": uploaded_file.getvalue()}
#     response = requests.post("http://127.0.0.1:5000/analyze", files=files)

#     if response.status_code == 200:
#         skills = response.json()["skills"]
#         st.write("### Extracted Skills")
#         st.write(", ".join(skills))
#     else:
#         st.error("Error analyzing the resume.")

import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    body {background-color: #eef5f9;}
    .main {background: linear-gradient(to right, #6a11cb, #2575fc); color: white; padding: 20px; border-radius: 10px; text-align: center;}
    .stTextInput, .stTextArea {border-radius: 10px; border: 2px solid #2575fc; padding: 8px;}
    .stButton>button {background: linear-gradient(to right, #ff416c, #ff4b2b); color: white; font-size: 18px; border-radius: 10px; padding: 12px 25px;}
    .stButton>button:hover {background: linear-gradient(to right, #ff4b2b, #ff416c);}
    .stFileUploader {border: 2px dashed #ff4b2b; padding: 10px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'><h1>📄 AI-Powered Resume Analyzer</h1><p>Upload your resume and match it with a job description to check compatibility.</p></div>", unsafe_allow_html=True)

# Upload File Section
st.subheader("📂 Upload Your Resume")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:5000/analyze", files=files)
    
    if response.status_code == 200:
        skills = response.json()["skills"]
        st.subheader("🎯 Extracted Skills")
        st.write("✔️ " + " | ✔️ ".join(skills))

        # Job Description Section
        st.subheader("📝 Enter Job Description")
        job_description = st.text_area("Paste Job Description here", height=150)
        
        if job_description:
            match_response = requests.post("http://127.0.0.1:5000/match", 
                                          json={"resume_text": uploaded_file.getvalue().decode("latin1"), 
                                                "job_description": job_description})
            if match_response.status_code == 200:
                match_data = match_response.json()
                
                st.subheader("📊 Match Results")
                st.markdown(f"<h2 style='text-align: center; color: #ff4b2b;'>Resume Match Score: {match_data['match_score']}%</h2>", unsafe_allow_html=True)
                
                st.write("### ❌ Missing Skills")
                st.write("❗ " + " | ❗ ".join(match_data["missing_skills"]))
                
                if st.button("📄 Generate PDF Report"):
                    report_response = requests.post("http://127.0.0.1:5000/generate-report", 
                                                   json={"resume_text": uploaded_file.getvalue().decode("latin1"), 
                                                         "skills": skills, 
                                                         "match_score": match_data["match_score"], 
                                                         "missing_skills": match_data["missing_skills"]})
                    if report_response.status_code == 200:
                        st.success("✅ Report Generated! Download below:")
                        st.download_button("📥 Download Report", report_response.content, "resume_report.pdf", "application/pdf")
