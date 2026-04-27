from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import Tuple, List, Dict, Any

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text (3+ chars)."""
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return list(set(words))

def keyword_match_score(resume: str, jd: str) -> Tuple[float, List[str], List[str]]:
    """Calculate keyword match score and return matched/missing keywords."""
    resume_words = set(extract_keywords(resume))
    jd_words = set(extract_keywords(jd))

    match = resume_words.intersection(jd_words)
    missing = jd_words - resume_words

    match_score = len(match) / max(len(jd_words), 1)
    return match_score, sorted(list(match)), sorted(list(missing))

def semantic_score(resume: str, jd: str) -> float:
    """Calculate semantic similarity using TF-IDF."""
    try:
        vectorizer = TfidfVectorizer(max_features=100).fit_transform([resume, jd])
        vectors = vectorizer.toarray()
        similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        return float(similarity)
    except:
        return 0.0

def calculate_ats_score(resume: str, jd: str) -> Dict[str, Any]:
    """Calculate ATS score with breakdown."""
    keyword_score, matched, missing = keyword_match_score(resume, jd)
    semantic = semantic_score(resume, jd)

    # Weighted calculation
    final_score = (keyword_score * 0.5 + semantic * 0.5)

    return {
        "ats_score": int(final_score * 100),
        "keyword_score": int(keyword_score * 100),
        "semantic_score": int(semantic * 100),
        "matched_keywords": matched[:25],
        "missing_keywords": missing[:25],
        "total_jd_keywords": len(missing) + len(matched),
        "match_percentage": int((len(matched) / max(len(matched) + len(missing), 1)) * 100)
    }

def generate_improvement_suggestions(resume: str, jd: str, score_data: Dict) -> Dict[str, List[str]]:
    """Generate suggestions for resume improvement."""
    suggestions = {
        "must_add": [],
        "should_improve": [],
        "nice_to_have": []
    }

    missing_keywords = score_data["missing_keywords"]

    # Technical keywords
    technical_keywords = [kw for kw in missing_keywords if kw in ['python', 'java', 'javascript', 'react', 'aws', 'docker', 'kubernetes', 'sql', 'api', 'rest', 'graphql']]

    if technical_keywords:
        suggestions["must_add"].append(f"Add technical skills: {', '.join(technical_keywords[:5])}")

    # Soft skills
    soft_skills = [kw for kw in missing_keywords if kw in ['leadership', 'communication', 'teamwork', 'collaboration', 'management', 'analytics', 'strategic']]

    if soft_skills:
        suggestions["should_improve"].append(f"Highlight soft skills: {', '.join(soft_skills[:3])}")

    # Score-based suggestions
    if score_data["ats_score"] < 50:
        suggestions["must_add"].append("Restructure resume to match job description format")
        suggestions["must_add"].append("Add quantifiable achievements and metrics")
    elif score_data["ats_score"] < 70:
        suggestions["should_improve"].append("Add more relevant keywords throughout experience section")
        suggestions["should_improve"].append("Highlight accomplishments with numbers/percentages")

    if score_data["match_percentage"] < 50:
        suggestions["must_add"].append(f"Missing {score_data['missing_keywords'][:3]} - add relevant experience or skills")

    if not re.search(r'\d+%|\$[\d,]+|[\d,]+\+', resume):
        suggestions["should_improve"].append("Add quantifiable metrics (percentages, numbers, dollar amounts)")

    suggestions["nice_to_have"].append("Add relevant certifications or courses")
    suggestions["nice_to_have"].append("Include links to projects or portfolio")

    return suggestions
