# analyzer.py
import io, re
import pdfplumber
from docx import Document
from sentence_transformers import SentenceTransformer, util
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load small embedding model (~90MB cached at HF cache)
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Default skill list — extend as needed
SKILLS_LIST = [
    "Python","Java","C++","SQL","Machine Learning","Deep Learning",
    "Data Analysis","Excel","Tableau","Docker","AWS","Git","React","Node.js",
    "Communication","Leadership","Teamwork"
]

def extract_text(uploaded_file):
    content = uploaded_file.read()
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for p in pdf.pages:
                page_text = p.extract_text() or ""
                text += page_text + "\n"
        return text
    elif name.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs if p.text])
    else:
        # plain text
        try:
            return content.decode("utf-8", errors="ignore")
        except:
            return str(content)

def compute_match_score(resume_text, jd_text):
    # limit length for safety
    r = resume_text[:20000]
    j = jd_text[:20000]
    r_emb = EMBED_MODEL.encode(r, convert_to_tensor=True)
    j_emb = EMBED_MODEL.encode(j, convert_to_tensor=True)
    sim = util.cos_sim(r_emb, j_emb).item()  # 0..1
    return round(sim * 100, 2)

def extract_skills(resume_text, skills_vocab=SKILLS_LIST):
    low = resume_text.lower()
    found = [s for s in skills_vocab if s.lower() in low]
    missing = [s for s in skills_vocab if s not in found]
    return found, missing

def build_suggestions(found, missing, score):
    # simple recruitery suggestions (no heavy LLM)
    strengths = ", ".join(found[:5]) if found else "No clear technical skills found."
    weaknesses = ", ".join(missing[:5]) if missing else "No major skill gaps from list."
    if score >= 75:
        note = "Strong fit — consider fast-tracking to interview."
    elif score >= 50:
        note = "Partial fit — may be good after targeted upskilling or screening."
    else:
        note = "Low fit — likely needs significant upskilling for this role."
    rec_lines = [
        f"Top strengths: {strengths}",
        f"Top missing skills: {weaknesses}",
        "Resume tips: Put most relevant skills in a 'Skills' section; mention concrete projects with metrics."
    ]
    return note, rec_lines

def generate_pdf_report_bytes(score, found, missing, suggestions_lines, resume_name="candidate"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(170, height - 50, "Resume Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Candidate File: {resume_name}")
    c.drawString(50, height - 110, f"Overall Match Score: {score}%")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 145, "Skills Found:")
    c.setFont("Helvetica", 11)
    c.drawString(160, height - 145, ", ".join(found) if found else "None")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 170, "Missing Skills:")
    c.setFont("Helvetica", 11)
    c.drawString(160, height - 170, ", ".join(missing) if missing else "None")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 200, "Recruiter Suggestions:")
    y = height - 220
    c.setFont("Helvetica", 11)
    for line in suggestions_lines:
        c.drawString(60, y, "- " + line)
        y -= 16
        if y < 80:
            c.showPage()
            y = height - 80

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
