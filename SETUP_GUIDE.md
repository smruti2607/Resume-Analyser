# 🚀 Complete Setup Guide for AI Resume Analyzer

This guide will help you get the AI Resume Analyzer up and running in 10 minutes.

## 📋 Prerequisites

- **Python 3.8+** (check with `python --version`)
- **pip** (comes with Python)
- **OpenAI API Key** (for LLM features)

## 🔑 Step 1: Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in to your OpenAI account
3. Click "Create new secret key"
4. Copy the key (save it securely!)
5. Keep this key ready for Step 3

> **Note:** You need a paid OpenAI account with credits. Free trial accounts may have limited access.

## 📁 Step 2: Project Structure

Make sure your folder structure looks like this:

```
resume-analyzer/
├── backend/
│   ├── main.py
│   ├── parser.py
│   ├── scorer.py
│   ├── llm.py
│   ├── pdf_generator.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
└── SETUP_GUIDE.md (this file)
```

## 🔧 Step 3: Configure Environment

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file:**
   ```env
   OPENAI_API_KEY=sk_your_key_here_paste_your_actual_key
   ```

3. **Replace `sk_your_key_here_paste_your_actual_key` with your actual OpenAI API key**

## 🚀 Step 4: Run Backend

**Terminal 1 - Backend Setup:**

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal running!**

## 🎨 Step 5: Run Frontend

**Terminal 2 - Frontend Setup (new terminal window):**

```bash
# Navigate to frontend directory
cd frontend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Streamlit
streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

A browser window will open automatically!

## ✅ Step 6: Test It!

1. **Upload a Resume**
   - Use a sample resume (PDF format)
   - Or create a simple text document, save as PDF

2. **Paste a Job Description**
   - Copy any job description from LinkedIn, Indeed, etc.

3. **Click "Analyze Resume"**
   - Wait 2-5 seconds for analysis
   - View your ATS Score and insights

4. **Try the Bonus Features**
   - Click "Rewrite Resume" to optimize
   - Click "Download Optimized Resume" to get PDF

## 🎯 Key Features to Try

| Feature | How to Use | Time |
|---------|-----------|------|
| **Analyze** | Upload resume + paste JD + click button | 2-5 sec |
| **Score Breakdown** | View pie chart and metrics | Instant |
| **Keywords** | See matched (green) vs missing (red) | Instant |
| **AI Coaching** | Read LLM-generated suggestions | Instant |
| **Rewrite Resume** | Click button, wait for AI generation | 10-15 sec |
| **Download PDF** | Click button, save optimized resume | 5 sec |

## 🐛 Troubleshooting

### Problem: "Cannot connect to backend"
**Solution:**
```bash
# Make sure backend is running
# Terminal 1 should show: "Uvicorn running on http://127.0.0.1:8000"
# If not running, go back to Step 4

# If port 8000 is busy:
lsof -i :8000
kill -9 <PID>
```

### Problem: "OPENAI_API_KEY not set"
**Solution:**
1. Check `.env` file exists in project root
2. Make sure it contains your actual key (not placeholder)
3. Restart Streamlit: press Ctrl+C, then `streamlit run app.py`

### Problem: "PDF extraction failed"
**Solution:**
- Make sure PDF is not encrypted
- Try a different PDF file
- Check PDF is less than 50MB

### Problem: "ModuleNotFoundError"
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Reinstall requirements
pip install -r requirements.txt
```

## 📊 What's Happening Behind the Scenes?

```
Your Resume (PDF) 
    ↓
[Parser] → Extract text
    ↓
[Scorer] → Calculate scores
    ├─ Keyword Matching (50%)
    └─ Semantic Similarity (50%)
    ↓
[LLM] → Generate feedback
    ├─ Analyze gaps
    ├─ Suggest improvements
    └─ Coach on next steps
    ↓
[UI] → Beautiful visualization
    ├─ Score gauges
    ├─ Keyword comparison
    ├─ AI recommendations
    └─ Resume rewrite
```

## 🚀 Next Steps

### Local Development
- Modify `scorer.py` to tweak scoring logic
- Edit `llm.py` to change coaching prompts
- Update `app.py` to customize UI

### Deploy to Cloud
1. **Backend**: Deploy to Heroku/Railway/Fly.io
2. **Frontend**: Deploy to Streamlit Cloud
3. See README.md for deployment instructions

### Add More Features
- Resume auto-parsing (extract structure)
- Multiple job description comparison
- Save analysis history
- User accounts and dashboards
- Integration with job boards

## 📚 Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **OpenAI API**: https://platform.openai.com/docs/
- **pdfplumber**: https://github.com/jsvine/pdfplumber

## ✨ Tips for Best Results

1. **Use high-quality resumes** - Clear formatting helps PDF extraction
2. **Paste full job descriptions** - More context = better analysis
3. **Review AI suggestions** - Don't blindly follow, use as guidance
4. **Test multiple roles** - See how scores vary across positions
5. **Share feedback** - Your insights help improve the tool

## 🎓 Educational Value

This project teaches:
- **FastAPI**: Modern Python web framework
- **Streamlit**: Quick data app creation
- **NLP**: Text processing, keyword extraction
- **ML**: Semantic similarity, scoring algorithms
- **LLM Integration**: Using GPT models for coaching
- **Full-stack**: Backend API + Frontend UI

## ❓ FAQs

**Q: Can I use this without OpenAI key?**
A: Yes, but LLM features (coaching, rewriting) won't work.

**Q: Is my data saved anywhere?**
A: No, everything stays local on your machine.

**Q: Can I modify the scoring?**
A: Yes! Edit `scorer.py` to change weights and logic.

**Q: How do I deploy this?**
A: See README.md deployment section.

**Q: What if I have a secret/private resume?**
A: Data never leaves your machine. Keep backend local.

---

**You're all set!** 🎉 

If you run into issues, check the troubleshooting section or review the README.md for more details.

Happy analyzing! 📄✨
