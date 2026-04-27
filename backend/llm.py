import os
from openai import OpenAI
import json
from typing import Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_feedback(resume: str, jd: str, score_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate LLM-powered coaching feedback."""

    if not os.getenv("OPENAI_API_KEY"):
        return {
            "error": "OpenAI API key not configured",
            "coaching": "Please set OPENAI_API_KEY in .env file"
        }

    prompt = f"""You are an expert career coach and recruiter. Analyze this resume against the job description.

RESUME (excerpt):
{resume[:1500]}

JOB DESCRIPTION (excerpt):
{jd[:1500]}

ATS SCORE: {score_data['ats_score']}%
MATCHED KEYWORDS: {', '.join(score_data['matched_keywords'][:10])}
MISSING KEYWORDS: {', '.join(score_data['missing_keywords'][:10])}

Provide ONLY valid JSON (no markdown, no extra text) with this structure:
{{
    "gap_analysis": "2-3 sentences about the main gaps",
    "key_improvements": ["improvement 1", "improvement 2", "improvement 3"],
    "skills_to_highlight": ["skill 1", "skill 2", "skill 3"],
    "action_items": ["action 1", "action 2", "action 3"],
    "overall_fit": "Poor/Fair/Good/Excellent match",
    "next_steps": "2-3 sentences on what to do next"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )

        feedback_text = response.choices[0].message.content
        feedback_json = json.loads(feedback_text)
        return feedback_json
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse LLM response",
            "raw_feedback": feedback_text if 'feedback_text' in locals() else "No response"
        }
    except Exception as e:
        return {
            "error": f"LLM Error: {str(e)}",
            "coaching": "Unable to generate coaching feedback at this time"
        }

def rewrite_resume(resume: str, jd: str, score_data: Dict[str, Any]) -> str:
    """Generate an optimized resume using LLM."""

    if not os.getenv("OPENAI_API_KEY"):
        return resume

    prompt = f"""You are an expert resume writer. Rewrite this resume to better match the job description while keeping it truthful.

ORIGINAL RESUME:
{resume[:2000]}

JOB DESCRIPTION:
{jd[:1500]}

MISSING KEYWORDS: {', '.join(score_data['missing_keywords'][:15])}

Instructions:
1. Rewrite bullet points to incorporate relevant missing keywords naturally
2. Emphasize quantifiable achievements
3. Rearrange experience to highlight most relevant roles
4. Use strong action verbs
5. Keep all information truthful - only reorganize and reword
6. Format as a plain text resume (keep line breaks for sections)

Return ONLY the rewritten resume text. No commentary."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=2000
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating rewrite: {str(e)}\n\nOriginal Resume:\n{resume}"

def chat_with_coach(user_message: str, resume: str, jd: str, score_data: Dict[str, Any]) -> str:
    """Interactive coaching chat with AI."""

    if not os.getenv("OPENAI_API_KEY"):
        return "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file."

    prompt = f"""You are an expert career coach and resume specialist. Have a conversation with the user about their resume and how to improve it for this job.

Context:
- User's Resume (excerpt): {resume[:1000]}
- Job Description (excerpt): {jd[:1000]}
- Current ATS Score: {score_data.get('ats_score', 'N/A')}%
- Matched Keywords: {', '.join(score_data.get('matched_keywords', [])[:10])}
- Missing Keywords: {', '.join(score_data.get('missing_keywords', [])[:10])}

User's Message: {user_message}

Instructions:
1. Be conversational and empathetic
2. Provide specific, actionable advice
3. If they disagree with suggestions, explain the rationale
4. Offer alternatives if they don't like the suggestions
5. Focus on truthfulness - never suggest fabricating experience
6. Be encouraging and supportive
7. Ask clarifying questions if needed
8. Provide concrete examples when possible

Keep your response concise (2-3 paragraphs max) and helpful."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error in coaching chat: {str(e)}"
