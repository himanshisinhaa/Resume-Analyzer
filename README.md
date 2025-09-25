# Resume-Analyzer

A smart, lightweight Resume Analyzer Web App built with Streamlit and Sentence Transformers.
This project helps recruiters quickly evaluate resumes against a job description, highlighting match score, key skills, gaps, and suggestions.

🚀 Features

🔎 Upload resumes (PDF/DOCX/TXT) and paste job description
📊 Get a Match Score (%) using semantic embeddings
✅ Identify Skills Found & Missing from a curated list
📝 Receive Recruiter Notes & Resume Tips
📥 Download a clean PDF Report
⚡ Runs fully on CPU (optimized for laptops, no GPU required)

🛠️ Tech Stack
Python 3
Streamlit – UI framework
pdfplumber – extract text from resumes
python-docx – handle DOCX resumes
sentence-transformers – semantic similarity model (MiniLM-L6-v2, CPU-friendly)
reportlab – PDF report generation

⚙️ Installation & Setup
1. Clone the repo
git clone https://github.com/<your-username>/resume-analyzer.git
cd resume-analyzer

2. Create a virtual environment
python -m venv venv
# Activate (Windows)
.\venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Run the app
streamlit run app.py


👉 Open http://localhost:8501
 in your browser.

📂 Project Structure
resume-analyzer/
│── app.py              # Streamlit UI
│── analyzer.py         # Resume analysis logic
│── requirements.txt    # Dependencies
│── README.md           # Documentation

📊 How It Works

Extracts raw text from the uploaded resume.
Encodes both resume & job description using MiniLM embeddings.
Computes a similarity-based Match Score.
Extracts skills → marks found vs. missing.
Generates recruiter notes and improvement tips.
Creates a downloadable PDF report.

💡 Future Enhancements

📑 Batch mode: upload multiple resumes → rank by fit
📊 Skill radar charts for visualization
🖥️ Recruiter dashboard for multiple JDs
🔗 Integration with ATS systems

👩‍💻 Author
📧 aks.sinha002@gmail.com

⭐ Show Support

If you found this project useful, please star the repo 🌟.
Recruiters: feedback is welcome — this tool was built to showcase real-world skills in Python + NLP + Web Apps.
