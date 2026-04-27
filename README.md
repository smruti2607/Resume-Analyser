# 📄 AI Resume Analyzer

An **Explainable AI Resume Analyzer** that combines rule-based ATS scoring with LLM-powered coaching.

## 🎯 Key Features

- **Not a Black Box**: Shows exactly why you got your score
- **Keyword Analysis**: See matched and missing keywords with visual tags
- **Score Breakdown**: Understand semantic + keyword components
- **AI Coaching**: LLM-powered suggestions for improvement via interactive chat
- **Resume Optimization**: Auto-generate optimized resume tailored to job description
- **Score Comparison**: Re-analyze optimized resume and compare scores side-by-side
- **PDF Download**: Export optimized resume as professionally formatted PDF
- **Beautiful UI**: Modern responsive dashboard with Enhancv color theme
- **Sidebar Menu**: Organized navigation for Dashboard, Keywords, Suggestions, AI Coach, and Rewrite
- **Real-time Feedback**: Instant analysis with detailed improvement suggestions

## 🏗️ Project Structure

```
resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── parser.py            # PDF extraction
│   ├── scorer.py            # ATS scoring logic
│   ├── llm.py               # LLM-powered coaching
│   ├── pdf_generator.py     # PDF export
│   └── requirements.txt
│
├── frontend/
│   ├── app.py               # Streamlit UI
│   └── requirements.txt
│
├── .env                     # Environment variables
├── README.md
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (for LLM features)

### 1. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Frontend

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

### 4. Run Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

The backend will start at `http://127.0.0.1:8000`

### 5. Run Frontend

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

The frontend will open at `http://localhost:8501`

## 📊 Features Breakdown

### ATS Scoring
- **Keyword Matching** (50%): Extracts keywords from job description and checks resume
- **Semantic Matching** (50%): Uses TF-IDF to understand content relevance
- **Final Score**: 0-100% based on weighted combination

### AI Coaching
- **Gap Analysis**: Identifies main differences between resume and JD
- **Key Improvements**: Specific improvements to make
- **Skills to Highlight**: Which skills matter most
- **Action Items**: Concrete next steps
- **Overall Fit**: Quick assessment of match quality

### Resume Optimization
- **Smart Rewriting**: Uses GPT-4o-mini to rewrite resume naturally
- **Keyword Integration**: Incorporates missing keywords where relevant
- **Truthfulness**: Only reorganizes content, never fabricates
- **PDF Export**: Download optimized resume immediately

## 🔧 API Endpoints

### POST `/analyze`
Analyze resume against job description.

**Parameters:**
- `file`: Resume PDF file
- `job_description`: Job description text

**Response:**
```json
{
  "score": {
    "ats_score": 75,
    "keyword_score": 80,
    "semantic_score": 70,
    "matched_keywords": [...],
    "missing_keywords": [...]
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
    "action_items": [...]
  }
}
```

### POST `/analyze-text`
Analyze resume text directly (without file upload).

**Parameters:**
- `resume_text`: Resume content as text
- `job_description`: Job description text

**Response:**
Same as `/analyze` endpoint

### POST `/rewrite-resume`
Generate optimized resume from PDF file.

**Parameters:**
- `file`: Resume PDF file
- `job_description`: Job description text

**Response:**
```json
{
  "original": "...",
  "rewritten": "...",
  "new_score": {
    "ats_score": 82,
    "keyword_score": 85,
    "semantic_score": 79
  }
}
```

### POST `/rewrite-text`
Generate optimized resume from text (recommended for re-analysis).

**Parameters:**
- `resume_text`: Resume content as text
- `job_description`: Job description text

**Response:**
Same as `/rewrite-resume`

### POST `/download-resume`
Download optimized resume as PDF.

**Parameters:**
- `file`: Original resume PDF file
- `job_description`: Job description text

## 💡 How It Works

### Standard Workflow
1. **Upload Resume**: User uploads PDF resume
2. **Paste Job Description**: User provides job description text
3. **Instant Analysis**:
   - Extract text from PDF
   - Calculate keyword match score (50%)
   - Calculate semantic similarity score (50%)
   - Generate LLM-powered feedback
   - Produce categorized improvement suggestions (Critical, Important, Nice-to-have)
4. **View Dashboard**: See metrics, matched/missing keywords, suggestions
5. **AI Coaching**: Chat with AI coach for personalized advice
6. **Optimize Resume**: Generate AI-optimized version

### Resume Optimization Workflow
1. **Generate Optimized Resume**: Click "Generate Optimized Resume" in Rewrite section
2. **View Comparison**: See original vs. new ATS score with improvement percentage
3. **Re-analyze**: Click "Re-Analyze Optimized Resume" to run full ATS analysis on new version
4. **Compare Results**: View detailed metrics comparison with delta values
5. **Download PDF**: Export the optimized resume as professional PDF
6. **Iterate**: Generate new versions until satisfied with results

## 🎓 Use Cases

- **Job Seekers**: Optimize resumes before applying
- **L&D Teams**: Coach employees on internal mobility
- **Career Advisors**: Provide data-driven feedback
- **Recruiters**: Understand candidate alignment

## ⚙️ Configuration

All configuration is done through environment variables in `.env`:

```env
# Required for LLM features
OPENAI_API_KEY=sk-...

# Backend (optional, defaults shown)
# BACKEND_URL=http://127.0.0.1:8000
```

## 📈 Performance

- **Analysis Time**: 2-5 seconds (excluding API calls)
- **Resume Rewrite**: 10-15 seconds (depends on OpenAI)
- **PDF Generation**: <1 second

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Make sure you're in backend directory
cd backend
# Kill any existing process on port 8000
lsof -i :8000  # Find process
kill -9 <PID>  # Kill it
# Try again
python -m uvicorn main:app --reload
```

### OpenAI API errors
- Check your API key in `.env`
- Ensure you have credits on your account
- Check OpenAI status: https://status.openai.com

### PDF extraction issues
- Ensure PDF is not encrypted
- Try with a different PDF to isolate issue

## 🚀 Deployment

### Deploy Backend (Heroku/Railway)
1. Create `Procfile`: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Set `OPENAI_API_KEY` as environment variable
3. Deploy and update `BACKEND_URL` in frontend

### Deploy Frontend (Streamlit Cloud)
1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect GitHub repo
4. Deploy and enjoy!

## 📝 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Fork, create a branch, and submit a PR.

## 📧 Contact

For questions or feedback, reach out!
