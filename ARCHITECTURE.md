# 🏗️ AI Resume Analyzer - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface (Streamlit)              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📤 Upload Resume  │  📝 Job Description  │  🔍 Analyze  │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  📊 Score Visualization  │  💡 Suggestions  │  📄 Rewrite  │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP (REST)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  POST /analyze          →  ATS Score + Feedback      │  │
│  │  POST /rewrite-resume   →  Optimized Resume Text     │  │
│  │  POST /download-resume  →  PDF File                  │  │
│  │  GET  /health           →  Backend Status            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Core Processing Modules                             │  │
│  │  ├─ parser.py: PDF extraction                        │  │
│  │  ├─ scorer.py: Keyword + semantic scoring            │  │
│  │  ├─ llm.py: OpenAI integration                       │  │
│  │  └─ pdf_generator.py: Resume PDF creation            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ API Key
                           ↓
        ┌──────────────────────────────────┐
        │   OpenAI API (GPT-4o-mini)       │
        │  - Generate coaching feedback    │
        │  - Rewrite resume               │
        │  - Analyze gaps                 │
        └──────────────────────────────────┘
```

## Data Flow

### Analysis Flow
```
1. User uploads PDF resume
   ↓
2. Parser extracts text from PDF
   │ Input: PDF file
   │ Output: Plain text resume
   ↓
3. Scorer calculates metrics
   │ Subprocess A: Keyword matching
   │   - Extract keywords from both
   │   - Find intersection
   │   - Calculate percentage
   │
   │ Subprocess B: Semantic similarity
   │   - TF-IDF vectorization
   │   - Cosine similarity
   │   - Get similarity score
   │
   │ Output: ATS Score (0-100%)
   ↓
4. Improvement suggestion generator
   │ Input: Resume + JD + Score Data
   │ Logic: Rule-based (thresholds, patterns)
   │ Output: Three-tier suggestions
   ↓
5. LLM feedback generator
   │ Input: Resume + JD + Score Data
   │ API Call: OpenAI ChatGPT
   │ Output: Structured coaching feedback
   ↓
6. Frontend receives all results
   │ Visualizes with charts
   │ Formats with nice UI
   │ Displays to user
   ↓
7. User sees complete analysis
```

### Resume Rewrite Flow
```
1. User clicks "Rewrite Resume"
   ↓
2. Backend receives original resume
   ↓
3. LLM (OpenAI) analyzes:
   - Original resume text
   - Job description
   - Missing keywords
   ↓
4. LLM generates optimized version:
   - Incorporates missing keywords naturally
   - Stronger action verbs
   - Quantifiable metrics
   - Better organization
   ↓
5. Recalculate ATS score on rewritten resume
   ↓
6. Return:
   - Original resume
   - Rewritten resume
   - New ATS score
   ↓
7. Frontend displays side-by-side comparison
```

## Component Details

### 1. Parser Module (`parser.py`)

**Responsibility**: Extract text from PDF documents

**Key Functions**:
- `extract_text_from_pdf(file)` → str
  - Uses pdfplumber library
  - Handles multi-page PDFs
  - Returns lowercase text
  - Error handling for corrupted PDFs

**Technologies**:
- pdfplumber: PDF text extraction

---

### 2. Scorer Module (`scorer.py`)

**Responsibility**: Calculate ATS score using two methods

**Key Functions**:

1. `extract_keywords(text)` → List[str]
   - Regex to find 3+ char words
   - Returns unique keywords
   
2. `keyword_match_score(resume, jd)` → Tuple
   - Resume keywords vs JD keywords
   - Returns: match percentage, matched list, missing list
   
3. `semantic_score(resume, jd)` → float
   - TF-IDF vectorization
   - Cosine similarity
   - Returns: 0-1 similarity score
   
4. `calculate_ats_score(resume, jd)` → Dict
   - Combines both metrics
   - 50% keyword + 50% semantic
   - Returns full score breakdown

**Scoring Logic**:
```
ATS Score = (Keyword Match × 0.5) + (Semantic Similarity × 0.5)
Range: 0-100%

Green (60-100%): Good fit, apply now
Yellow (30-60%): Fair fit, needs work
Red (0-30%): Poor fit, consider other roles
```

**Technologies**:
- scikit-learn: TF-IDF vectorization, cosine similarity

---

### 3. LLM Module (`llm.py`)

**Responsibility**: Generate coaching feedback and rewrite resumes

**Key Functions**:

1. `generate_feedback(resume, jd, score_data)` → Dict
   - Sends prompt to OpenAI
   - Returns: Gap analysis, improvements, skills, action items
   - Includes: Overall fit assessment, next steps
   
2. `rewrite_resume(resume, jd, score_data)` → str
   - Instructs LLM to rewrite resume
   - Uses context from JD and missing keywords
   - Guarantees truthfulness
   - Returns optimized text

**Prompt Engineering**:
- Specific instructions for consistency
- JSON format for structured output
- Temperature: 0.3 (deterministic)
- Max tokens: 1000-2000

**Technologies**:
- OpenAI API: GPT-4o-mini model
- JSON parsing for structured responses

---

### 4. PDF Generator Module (`pdf_generator.py`)

**Responsibility**: Create formatted PDF from resume text

**Key Functions**:
- `generate_resume_pdf(text)` → BytesIO
  - Uses ReportLab for styling
  - Section detection (UPPERCASE)
  - Professional formatting
  - Returns PDF in memory

**Formatting**:
- Section headers: Blue, bold, larger font
- Body text: 10pt, proper spacing
- Margins: 0.5 inches
- Professional typography

**Technologies**:
- ReportLab: PDF generation library

---

### 5. FastAPI Server (`main.py`)

**Responsibility**: REST API endpoints

**Endpoints**:

```
POST /analyze
├─ Input: resume PDF, job description text
├─ Process: Extract → Score → Suggest → Feedback
└─ Output: {score, suggestions, feedback}

POST /rewrite-resume
├─ Input: resume PDF, job description text
├─ Process: Extract → Rewrite → Rescore
└─ Output: {original, rewritten, new_score}

POST /download-resume
├─ Input: resume PDF, job description text
├─ Process: Extract → Rewrite → Generate PDF
└─ Output: PDF file (binary)

GET /health
├─ No input
├─ Check: Server status
└─ Output: {status: "ok"}
```

**Technologies**:
- FastAPI: Async Python web framework
- Uvicorn: ASGI server
- python-dotenv: Environment variable management

---

### 6. Streamlit Frontend (`app.py`)

**Responsibility**: User interface and visualization

**Key Sections**:

1. **Header & Configuration**
   - Branding and description
   - Backend status check
   - API key status indicator

2. **Input Section**
   - File uploader for resume
   - Text area for job description
   - Analyze button

3. **Results Display**
   - Metric cards (ATS, Keyword, Semantic)
   - Plotly charts (gauge, breakdown, comparison)
   - Score breakdown pie chart

4. **Suggestions Display**
   - Three-tier card layout (Must Add, Should Improve, Nice to Have)
   - Color-coded (Red, Orange, Green)
   - Bulleted list format

5. **AI Feedback Display**
   - Overall fit badge
   - Gap analysis
   - Key improvements (bulleted)
   - Skills to highlight
   - Action items (numbered)
   - Next steps

6. **Resume Optimization**
   - Rewrite button
   - Download PDF button
   - Rewritten resume preview
   - Score comparison

**Technologies**:
- Streamlit: Web app framework
- Plotly: Interactive charts
- Requests: HTTP API calls

---

## API Specifications

### POST /analyze

**Request**:
```
Content-Type: multipart/form-data

file: [PDF binary]
job_description: [string]
```

**Response**:
```json
{
  "score": {
    "ats_score": 75,
    "keyword_score": 80,
    "semantic_score": 70,
    "matched_keywords": ["python", "react", ...],
    "missing_keywords": ["kubernetes", "gcp", ...],
    "total_jd_keywords": 45,
    "match_percentage": 64
  },
  "suggestions": {
    "must_add": [...],
    "should_improve": [...],
    "nice_to_have": [...]
  },
  "feedback": {
    "gap_analysis": "...",
    "key_improvements": [...],
    "skills_to_highlight": [...],
    "action_items": [...],
    "overall_fit": "Good",
    "next_steps": "..."
  }
}
```

---

## Technology Stack

### Backend
| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | FastAPI | REST API |
| Server | Uvicorn | ASGI application server |
| PDF Processing | pdfplumber | Extract text from PDFs |
| NLP | scikit-learn | TF-IDF, cosine similarity |
| LLM | OpenAI API | GPT-4o-mini for coaching |
| PDF Generation | ReportLab | Create styled PDFs |
| Configuration | python-dotenv | Load environment variables |

### Frontend
| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | Streamlit | Web app development |
| Visualization | Plotly | Interactive charts |
| HTTP Client | Requests | API communication |
| Styling | Markdown + CSS | Custom styling |

---

## Performance Characteristics

### Scoring Algorithm
- **Keyword Extraction**: O(n) where n = text length
- **Keyword Matching**: O(k) where k = unique keywords
- **TF-IDF Vectorization**: O(n × m) where n, m = document lengths
- **Cosine Similarity**: O(v²) where v = vector dimensions

**Total Scoring Time**: <1 second

### LLM Operations
- **API Latency**: 5-10 seconds (network dependent)
- **Token Generation**: 10-15 seconds for resume rewrite
- **Throughput**: Depends on OpenAI quota

### Memory Usage
- **Resume Text**: ~100-500 KB
- **PDF Processing**: ~1-10 MB
- **TF-IDF Vectors**: ~100 KB
- **Total**: <50 MB per request

---

## Error Handling

### PDF Extraction
```
Valid PDF → Text ✅
Corrupted PDF → Error message
Encrypted PDF → Error message
Empty PDF → Handled gracefully
```

### Scoring
```
Valid text → Score ✅
Empty text → Score = 0
Special characters → Cleaned automatically
```

### LLM
```
Valid API key → Feedback ✅
Invalid key → Error message
Rate limit → Backoff/retry
Network error → Graceful fallback
JSON parse error → Raw feedback fallback
```

---

## Deployment Architecture

### Local Development
```
Frontend (localhost:8501) ← HTTP → Backend (localhost:8000)
                                      ↓
                              OpenAI API
```

### Cloud Deployment (Example)
```
Streamlit Cloud → HTTP → Railway/Heroku Backend → OpenAI API
```

---

## Security Considerations

1. **API Key Management**
   - Stored in `.env` (local only)
   - Never in code or version control
   - Graceful degradation if missing

2. **Input Validation**
   - File type checking (PDF only)
   - File size limits (implicit)
   - Text input sanitization

3. **Data Privacy**
   - No data persistence (unless explicitly added)
   - No logging of sensitive content
   - Local processing by default

4. **API Security**
   - HTTPS for production
   - CORS configuration for deployment
   - Rate limiting (OpenAI handles)

---

## Scalability Considerations

### Current Limits
- Single backend instance
- Single process execution
- Synchronous LLM calls

### Scaling Strategies
1. **Async Processing**
   - Queue system (Celery/RQ)
   - Background job processing
   - Webhook callbacks

2. **Distributed Backend**
   - Multiple backend instances
   - Load balancer
   - Shared caching layer

3. **LLM Optimization**
   - Prompt caching
   - Batch processing
   - Model fine-tuning

---

## Testing Strategy

### Unit Tests (To be added)
- Parser: Extract text correctly
- Scorer: Calculate scores accurately
- Suggestion generator: Produce correct tier assignments
- PDF generator: Create valid PDFs

### Integration Tests (To be added)
- End-to-end analysis flow
- API response validation
- Frontend + Backend interaction

### Performance Tests (To be added)
- Large resume handling
- Long job description processing
- Concurrent request handling

---

## Future Enhancements

1. **Database Integration**
   - Store analysis history
   - User accounts
   - Resume versions

2. **Advanced Features**
   - Multiple job description comparison
   - Industry-specific scoring
   - Skill gap learning paths
   - Interview prep based on gaps

3. **Deployment**
   - Docker containerization
   - Kubernetes orchestration
   - Managed service deployment

4. **Analytics**
   - User metrics
   - Popular skills by role
   - Industry benchmarks

---

## Conclusion

The AI Resume Analyzer is a well-architected system combining:
- **Rule-based scoring** for transparency
- **ML algorithms** for semantic understanding
- **LLM coaching** for intelligent feedback
- **Beautiful UI** for user experience

All components work together to provide actionable, explainable resume optimization.
