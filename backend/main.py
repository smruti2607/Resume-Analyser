from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os
import json
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

from parser import extract_text_from_pdf, parse_resume_sections
from scorer import calculate_ats_score, generate_improvement_suggestions
from llm import generate_feedback, rewrite_resume
from pdf_generator import generate_resume_pdf

# Load .env from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

app = FastAPI(title="AI Resume Analyzer")

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Analyze resume against job description."""
    resume_text = extract_text_from_pdf(file.file)
    jd_text = job_description.lower()

    # Score and analyze
    score_data = calculate_ats_score(resume_text, jd_text)
    suggestions = generate_improvement_suggestions(resume_text, jd_text, score_data)
    feedback = generate_feedback(resume_text, jd_text, score_data)

    return {
        "score": score_data,
        "suggestions": suggestions,
        "feedback": feedback,
        "resume_text": resume_text
    }

@app.post("/analyze-text")
async def analyze_text(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    """Analyze resume text against job description."""
    jd_text = job_description.lower()

    # Score and analyze
    score_data = calculate_ats_score(resume_text, jd_text)
    suggestions = generate_improvement_suggestions(resume_text, jd_text, score_data)
    feedback = generate_feedback(resume_text, jd_text, score_data)

    return {
        "score": score_data,
        "suggestions": suggestions,
        "feedback": feedback
    }

@app.post("/rewrite-resume")
async def rewrite_resume_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Generate optimized resume."""
    try:
        resume_text = extract_text_from_pdf(file.file)
        jd_text = job_description.lower()

        score_data = calculate_ats_score(resume_text, jd_text)
        rewritten = rewrite_resume(resume_text, jd_text, score_data)

        return {
            "original": resume_text,
            "rewritten": rewritten,
            "new_score": calculate_ats_score(rewritten, jd_text)
        }
    except Exception as e:
        return {
            "error": str(e),
            "details": f"Failed to rewrite resume: {str(e)}"
        }

@app.post("/rewrite-text")
async def rewrite_text_endpoint(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    """Generate optimized resume from text."""
    try:
        jd_text = job_description.lower()
        score_data = calculate_ats_score(resume_text, jd_text)
        rewritten = rewrite_resume(resume_text, jd_text, score_data)

        return {
            "original": resume_text,
            "rewritten": rewritten,
            "new_score": calculate_ats_score(rewritten, jd_text)
        }
    except Exception as e:
        return {
            "error": str(e),
            "details": f"Failed to rewrite resume: {str(e)}"
        }

@app.post("/download-resume")
async def download_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Download optimized resume as PDF."""
    resume_text = extract_text_from_pdf(file.file)
    jd_text = job_description.lower()

    score_data = calculate_ats_score(resume_text, jd_text)
    rewritten = rewrite_resume(resume_text, jd_text, score_data)

    pdf_buffer = generate_resume_pdf(rewritten)

    return FileResponse(
        pdf_buffer,
        media_type="application/pdf",
        filename="optimized_resume.pdf"
    )

@app.post("/coaching-chat")
async def coaching_chat(
    user_message: str = Form(...),
    resume_text: str = Form(...),
    job_description: str = Form(...),
    score_data: str = Form(...)
):
    """Chat with AI coach for personalized feedback."""
    from llm import chat_with_coach

    try:
        score_dict = json.loads(score_data)
    except:
        score_dict = {}

    response = chat_with_coach(user_message, resume_text, job_description, score_dict)
    return {"response": response}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
