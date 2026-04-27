import pdfplumber
from typing import Tuple

def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file."""
    text = ""
    try:
        # Seek to beginning in case file was already read
        if hasattr(file, 'seek'):
            file.seek(0)
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.lower()
    except Exception as e:
        raise ValueError(f"Error extracting PDF: {str(e)}")

def parse_resume_sections(resume_text: str) -> dict:
    """Parse resume into sections: contact, summary, experience, skills, education."""
    sections = {
        "full_text": resume_text,
        "has_contact": any(keyword in resume_text for keyword in ["email", "@", "phone", "linkedin"]),
        "has_experience": any(keyword in resume_text for keyword in ["experience", "work", "employment", "role", "position"]),
        "has_skills": any(keyword in resume_text for keyword in ["skills", "technical", "proficiency", "expertise"]),
        "has_education": any(keyword in resume_text for keyword in ["education", "degree", "university", "college", "bachelor", "master"])
    }
    return sections
