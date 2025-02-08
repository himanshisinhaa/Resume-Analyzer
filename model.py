# import spacy
# import pdfplumber

# # Load NLP model
# nlp = spacy.load("en_core_web_sm")

# # Extract text from PDF
# def extract_text_from_pdf(pdf_path):
#     with pdfplumber.open(pdf_path) as pdf:
#         text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
#     print(f"✅ Extracted Resume Text:\n{text[:500]}")  # Debugging
#     return text

# # Extract skills and experience
# def analyze_resume(text):
#     doc = nlp(text)
#     skills = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE"]]
#     return list(set(skills))

# # Example usage
# if __name__ == "__main__":
#     text = extract_text_from_pdf("example_resume.pdf")
#     skills = analyze_resume(text)
#     print("Extracted Skills:", skills)


import spacy
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def analyze_resume(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "GPE"]]
    return list(set(skills))

def match_with_job(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())
    missing_skills = list(job_words - resume_words)
    return round(similarity[0][0] * 100, 2), missing_skills

def generate_pdf_report(resume_text, skills, match_score, missing_skills):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Resume Analysis Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Match Score: {match_score}%", ln=True)
    pdf.cell(200, 10, "Extracted Skills:", ln=True)
    pdf.multi_cell(0, 10, ", ".join(skills))
    if missing_skills:
        pdf.cell(200, 10, "Missing Skills:", ln=True)
        pdf.multi_cell(0, 10, ", ".join(missing_skills))
    report_path = "reports/resume_report.pdf"
    pdf.output(report_path)
    return report_path