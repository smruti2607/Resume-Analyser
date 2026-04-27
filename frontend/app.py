import streamlit as st
import requests
import json
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Color Theme with Enhancv palette
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF2F5 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .main {
            padding: 0;
            background: linear-gradient(135deg, #F8FAFC 0%, #EEF2F5 100%);
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #3685BB 0%, #57CDA4 100%);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 20px;
            margin: 2rem;
            box-shadow: 0 10px 40px rgba(54, 133, 187, 0.25);
            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: rgba(255, 224, 185, 0.1);
            border-radius: 50%;
        }

        .hero::after {
            content: '';
            position: absolute;
            bottom: -30%;
            left: -5%;
            width: 300px;
            height: 300px;
            background: rgba(87, 205, 164, 0.1);
            border-radius: 50%;
        }

        .hero-content {
            position: relative;
            z-index: 1;
        }

        .hero h1 {
            font-size: 3.2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .hero p {
            font-size: 1.3rem;
            opacity: 0.95;
            margin-bottom: 0.3rem;
            font-weight: 500;
        }

        .hero-tagline {
            font-size: 1rem;
            opacity: 0.85;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 2px solid rgba(255, 255, 255, 0.2);
        }

        /* Step Indicators */
        .steps-container {
            display: flex;
            justify-content: space-around;
            margin: 3rem 2rem;
            gap: 20px;
        }

        .step {
            flex: 1;
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            border: 2px solid #E2E8F0;
            transition: all 0.3s ease;
        }

        .step:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(54, 133, 187, 0.15);
            border-color: #57CDA4;
        }

        .step-number {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #3685BB 0%, #57CDA4 100%);
            color: white;
            border-radius: 50%;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .step-title {
            font-size: 16px;
            font-weight: 600;
            color: #2D3639;
            margin-bottom: 8px;
        }

        .step-description {
            font-size: 13px;
            color: #666;
            line-height: 1.5;
        }

        /* Upload Section */
        .upload-container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }

        .upload-card {
            background: white;
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            border: 2px solid #E2E8F0;
        }

        .upload-card h2 {
            color: #3685BB;
            font-size: 28px;
            margin-bottom: 2rem;
            text-align: center;
        }

        .input-group {
            margin-bottom: 2rem;
        }

        .input-group label {
            display: block;
            font-size: 15px;
            font-weight: 600;
            color: #2D3639;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .input-group .help-text {
            font-size: 12px;
            color: #999;
            font-weight: 400;
            margin-top: 5px;
        }

        /* Results Section */
        .results-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        .results-header {
            background: linear-gradient(135deg, #3685BB 0%, #57CDA4 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 24px rgba(54, 133, 187, 0.2);
        }

        .results-header h2 {
            font-size: 28px;
            margin-bottom: 10px;
        }

        /* Metrics Grid */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }

        @media (max-width: 1200px) {
            .metrics-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .metrics-grid {
                grid-template-columns: repeat(1, 1fr);
            }
        }

        .metric-card {
            background: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            border: 2px solid #E2E8F0;
            transition: all 0.3s ease;
            text-align: center;
        }

        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(54, 133, 187, 0.15);
            border-color: #57CDA4;
        }

        .metric-icon {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .metric-value {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #3685BB 0%, #57CDA4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 8px 0;
        }

        .metric-label {
            font-size: 13px;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Content Sections */
        .content-section {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            margin-bottom: 2rem;
            border-top: 4px solid #57CDA4;
        }

        .content-section h3 {
            color: #3685BB;
            font-size: 20px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Keyword Tags */
        .keyword-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }

        .keyword-tag {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            transition: all 0.2s ease;
        }

        .keyword-tag:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        }

        .tag-matched {
            background: linear-gradient(135deg, #57CDA4 0%, #249A71 100%);
            color: white;
        }

        .tag-missing {
            background: linear-gradient(135deg, #A396E2 0%, #5F3DC4 100%);
            color: white;
        }

        /* Suggestion Cards */
        .suggestion-card {
            padding: 18px;
            border-left: 4px solid #57CDA4;
            background: linear-gradient(135deg, #F0FDF7 0%, #F5FDF9 100%);
            border-radius: 8px;
            margin: 12px 0;
            transition: all 0.2s;
        }

        .suggestion-card:hover {
            box-shadow: 0 4px 12px rgba(87, 205, 164, 0.15);
        }

        .suggestion-card.critical {
            border-left-color: #E74C3C;
            background: linear-gradient(135deg, #FFE8E8 0%, #FFF0F0 100%);
        }

        .suggestion-card.important {
            border-left-color: #FFB347;
            background: linear-gradient(135deg, #FFF9F0 0%, #FFFAF5 100%);
        }

        /* Chat Interface */
        .chat-section {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            border-top: 4px solid #57CDA4;
        }

        .chat-messages {
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 15px;
            background: #F8FAFC;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
        }

        .message {
            margin-bottom: 15px;
            display: flex;
            gap: 10px;
        }

        .message.user {
            justify-content: flex-end;
        }

        .message-bubble {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 13px;
            line-height: 1.6;
            word-wrap: break-word;
        }

        .message.user .message-bubble {
            background: linear-gradient(135deg, #3685BB 0%, #57CDA4 100%);
            color: white;
        }

        .message.assistant .message-bubble {
            background: #E8EFF7;
            color: #2D3639;
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3685BB 0%, #57CDA4 100%) !important;
            color: white !important;
            border: none !important;
            padding: 14px 32px !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(54, 133, 187, 0.3) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(54, 133, 187, 0.4) !important;
        }

        /* Sidebar Menu */
        [data-testid="stSidebar"] {
            background: white;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.08);
        }

        [data-testid="stSidebar"] h3 {
            color: #3685BB;
            font-size: 20px;
            margin-bottom: 20px;
            font-weight: 700;
        }

        .sidebar-menu-item {
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

def show_hero():
    """Show hero section."""
    st.markdown("""
        <div class="hero">
            <div class="hero-content">
                <h1>📄 AI Resume Analyzer</h1>
                <p>Get Instant Feedback on Your Resume</p>
                <div class="hero-tagline">
                    Understand your ATS score • Discover missing keywords • Get AI-powered coaching
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_steps():
    """Show step indicators."""
    st.markdown("""
        <div class="steps-container">
            <div class="step">
                <div class="step-number">1️⃣</div>
                <div class="step-title">Upload Resume</div>
                <div class="step-description">Share your PDF resume</div>
            </div>
            <div class="step">
                <div class="step-number">2️⃣</div>
                <div class="step-title">Paste Job Description</div>
                <div class="step-description">Copy from any job posting</div>
            </div>
            <div class="step">
                <div class="step-number">3️⃣</div>
                <div class="step-title">Get Instant Analysis</div>
                <div class="step-description">See scores & suggestions</div>
            </div>
            <div class="step">
                <div class="step-number">4️⃣</div>
                <div class="step-title">Chat with AI Coach</div>
                <div class="step-description">Discuss improvements</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_gauge(score: int, label: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=score,
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#3685BB"},
            "steps": [
                {"range": [0, 30], "color": "#F0E8E8"},
                {"range": [30, 60], "color": "#FFF9F0"},
                {"range": [60, 100], "color": "#F0FDF7"}
            ],
        },
        number={"suffix": "%"},
        title={"text": label}
    ))
    fig.update_layout(height=300, margin={"l": 20, "r": 20, "t": 40, "b": 20}, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

def main():
    # Initialize session state
    if "current_menu" not in st.session_state:
        st.session_state.current_menu = "home"

    # Sidebar Menu
    with st.sidebar:
        st.markdown("<h3 style='color: #3685BB; font-size: 22px; margin-bottom: 20px;'>📋 Menu</h3>", unsafe_allow_html=True)

        if st.session_state.get("show_results"):
            menu_option = st.radio(
                "Navigation",
                ["🤖 AI Coach", "📝 Rewrite"],
                key="menu_radio",
                label_visibility="collapsed",
                index=0 if st.session_state.current_menu == "coach" else
                      1 if st.session_state.current_menu == "rewrite" else 0
            )

            if menu_option == "🤖 AI Coach":
                st.session_state.current_menu = "coach"
            elif menu_option == "📝 Rewrite":
                st.session_state.current_menu = "rewrite"

            st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
            if st.button("🔄 New Analysis", use_container_width=True):
                st.session_state.show_results = False
                st.session_state.chat_history = []
                st.session_state.current_menu = "home"
                if "rewritten" in st.session_state:
                    del st.session_state.rewritten
                st.rerun()
        else:
            st.info("💡 Upload a resume to see the menu options")

    # Home Page
    if not st.session_state.get("show_results"):
        show_hero()
        show_steps()

        st.markdown("<div class='upload-container'>", unsafe_allow_html=True)
        st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
        st.markdown("<h2>🚀 Analyze Your Resume</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("<div class='input-group'>", unsafe_allow_html=True)
            st.markdown("<label>📄 Your Resume (PDF)</label>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
            st.markdown("<div class='help-text'>Upload your PDF resume. We'll analyze it instantly.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='input-group'>", unsafe_allow_html=True)
            st.markdown("<label>📋 Job Description</label>", unsafe_allow_html=True)
            jd = st.text_area("", height=120, placeholder="Paste the job description from LinkedIn, Indeed, or any job posting...", label_visibility="collapsed")
            st.markdown("<div class='help-text'>Paste the complete job description for accurate analysis.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_btn = st.button("🎯 Analyze My Resume", use_container_width=True, type="primary")

        st.markdown("</div></div>", unsafe_allow_html=True)

        if analyze_btn:
            if not uploaded_file or not jd:
                st.error("⚠️ Please upload your resume and paste the job description to get started.")
            else:
                with st.spinner("🔍 Analyzing your resume..."):
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/analyze",
                            files={"file": uploaded_file},
                            data={"job_description": jd},
                            timeout=30
                        )

                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.resume_data = {
                                "score_data": result["score"],
                                "suggestions": result["suggestions"],
                                "feedback": result["feedback"],
                                "file": uploaded_file,
                                "jd": jd,
                                "resume_text": result.get("resume_text", "")
                            }
                            st.session_state.show_results = True
                            st.session_state.current_menu = "dashboard"
                            st.success("✅ Analysis Complete!")
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

    # Results Pages
    else:
        st.markdown("<div class='results-container'>", unsafe_allow_html=True)

        data = st.session_state.resume_data
        score_data = data["score_data"]

        st.markdown("""
            <div class='results-header'>
                <h2>📊 Your Resume Analysis</h2>
                <p>Here's what we found and how to improve</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-icon'>🎯</div>
                    <div class='metric-value'>{score_data['ats_score']}%</div>
                    <div class='metric-label'>ATS Score</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-icon'>🔤</div>
                    <div class='metric-value'>{score_data['keyword_score']}%</div>
                    <div class='metric-label'>Keyword Match</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-icon'>🧠</div>
                    <div class='metric-value'>{score_data['semantic_score']}%</div>
                    <div class='metric-label'>Content Match</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-icon'>✅</div>
                    <div class='metric-value'>{len(score_data['matched_keywords'])}</div>
                    <div class='metric-label'>Keywords Found</div>
                </div>
            """, unsafe_allow_html=True)

        # Always show Dashboard, Keywords, and Suggestions
        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        st.markdown("<h3>📈 Score Overview</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_gauge(score_data['ats_score'], "ATS Score"), use_container_width=True, config={"displayModeBar": False})
        with col2:
            st.plotly_chart(create_gauge(score_data['keyword_score'], "Keyword Match"), use_container_width=True, config={"displayModeBar": False})

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        st.markdown("<h3>🔍 Keyword Analysis</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='color: #57CDA4; margin-bottom: 15px;'>✅ Keywords Found</h4>", unsafe_allow_html=True)
            keywords_html = "".join([f'<span class="keyword-tag tag-matched">✓ {kw}</span>' for kw in score_data["matched_keywords"][:15]])
            st.markdown(f"<div class='keyword-container'>{keywords_html}</div>", unsafe_allow_html=True)
            st.caption(f"Found {len(score_data['matched_keywords'])} keywords")

        with col2:
            st.markdown("<h4 style='color: #5F3DC4; margin-bottom: 15px;'>❌ Missing Keywords</h4>", unsafe_allow_html=True)
            keywords_html = "".join([f'<span class="keyword-tag tag-missing">✗ {kw}</span>' for kw in score_data["missing_keywords"][:15]])
            st.markdown(f"<div class='keyword-container'>{keywords_html}</div>", unsafe_allow_html=True)
            st.caption(f"Missing {len(score_data['missing_keywords'])} keywords")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='content-section'>", unsafe_allow_html=True)
        st.markdown("<h3>💡 Improvement Suggestions</h3>", unsafe_allow_html=True)

        if data["suggestions"]["must_add"]:
            st.markdown("<h4 style='color: #E74C3C; margin-top: 20px;'>🔴 Critical Improvements</h4>", unsafe_allow_html=True)
            for s in data["suggestions"]["must_add"]:
                st.markdown(f"<div class='suggestion-card critical'>{s}</div>", unsafe_allow_html=True)

        if data["suggestions"]["should_improve"]:
            st.markdown("<h4 style='color: #FFB347; margin-top: 20px;'>🟡 Important Improvements</h4>", unsafe_allow_html=True)
            for s in data["suggestions"]["should_improve"]:
                st.markdown(f"<div class='suggestion-card important'>{s}</div>", unsafe_allow_html=True)

        if data["suggestions"]["nice_to_have"]:
            st.markdown("<h4 style='color: #57CDA4; margin-top: 20px;'>🟢 Nice to Have</h4>", unsafe_allow_html=True)
            for s in data["suggestions"]["nice_to_have"]:
                st.markdown(f"<div class='suggestion-card'>{s}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)

        # AI Coach
        if st.session_state.current_menu == "coach":
            st.markdown("<div class='chat-section'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #3685BB;'>💬 Chat with Your AI Coach</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; font-size: 14px; margin-bottom: 20px;'>Discuss your resume and get personalized coaching. Don't agree with a suggestion? Ask for alternatives!</p>", unsafe_allow_html=True)

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            st.markdown("<div class='chat-messages'>", unsafe_allow_html=True)
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"<div class='message user'><div class='message-bubble'>{msg['content']}</div></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='message assistant'><div class='message-bubble'>{msg['content']}</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            col1, col2 = st.columns([5, 1])
            with col1:
                user_input = st.text_input("Ask your coach...", placeholder="e.g., How can I present this differently?", label_visibility="collapsed")
            with col2:
                send_btn = st.button("Send", use_container_width=True)

            if send_btn and user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("🤖 Coach is thinking..."):
                    try:
                        import pdfplumber
                        from io import BytesIO
                        pdf_file = BytesIO(data["file"].read())
                        resume_text = ""
                        with pdfplumber.open(pdf_file) as pdf:
                            for page in pdf.pages:
                                resume_text += page.extract_text() or ""

                        response = requests.post(
                            f"{BACKEND_URL}/coaching-chat",
                            data={
                                "user_message": user_input,
                                "resume_text": resume_text,
                                "job_description": data["jd"],
                                "score_data": json.dumps(score_data)
                            },
                            timeout=30
                        )

                        if response.status_code == 200:
                            result = response.json()
                            st.session_state.chat_history.append({"role": "assistant", "content": result.get("response")})
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

            st.markdown("</div>", unsafe_allow_html=True)

        # Rewrite
        elif st.session_state.current_menu == "rewrite":
            st.markdown("<div class='content-section'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #3685BB;'>📝 AI Resume Rewrite</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; margin-bottom: 20px;'>Get an AI-optimized version of your resume tailored to this job description.</p>", unsafe_allow_html=True)

            if not st.session_state.get("rewritten"):
                if st.button("✨ Generate Optimized Resume", use_container_width=True, type="primary"):
                    with st.spinner("✍️ Generating optimized resume..."):
                        try:
                            response = requests.post(
                                f"{BACKEND_URL}/rewrite-text",
                                data={
                                    "resume_text": data.get("resume_text", ""),
                                    "job_description": data["jd"]
                                },
                                timeout=60
                            )

                            if response.status_code == 200:
                                result = response.json()
                                if "error" in result:
                                    st.error(f"Error: {result.get('details', result['error'])}")
                                elif "rewritten" in result:
                                    st.session_state.rewritten = result["rewritten"]
                                    st.session_state.new_score = result["new_score"]
                                    st.success("✅ Resume optimized!")
                                    st.rerun()
                                else:
                                    st.error(f"Unexpected response: {result}")
                            else:
                                st.error(f"Error: {response.status_code}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

            else:
                # Show comparison
                st.subheader("📊 Score Comparison")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("""
                        <div class='metric-card'>
                            <div class='metric-icon'>📄</div>
                            <div class='metric-value' style='font-size: 2rem;'>{}</div>
                            <div class='metric-label'>Original Score</div>
                        </div>
                    """.format(score_data['ats_score']), unsafe_allow_html=True)

                with col2:
                    improvement = st.session_state.new_score['ats_score'] - score_data['ats_score']
                    color = "#57CDA4" if improvement >= 0 else "#E74C3C"
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-icon'>📈</div>
                            <div class='metric-value' style='font-size: 2rem; color: {color};'>{improvement:+d}%</div>
                            <div class='metric-label'>Improvement</div>
                        </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown("""
                        <div class='metric-card'>
                            <div class='metric-icon'>✨</div>
                            <div class='metric-value' style='font-size: 2rem;'>{}</div>
                            <div class='metric-label'>New Score</div>
                        </div>
                    """.format(st.session_state.new_score['ats_score']), unsafe_allow_html=True)

                st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

                # Show optimized resume
                st.subheader("📄 Optimized Resume")
                st.text_area("", value=st.session_state.rewritten, height=400, disabled=True, label_visibility="collapsed")

                st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

                # Action buttons
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("🔄 Re-Analyze Optimized Resume", use_container_width=True, key="reanalyze_btn"):
                        with st.spinner("🔍 Re-analyzing optimized resume..."):
                            try:
                                response = requests.post(
                                    f"{BACKEND_URL}/analyze-text",
                                    data={
                                        "job_description": data["jd"],
                                        "resume_text": st.session_state.rewritten
                                    },
                                    timeout=30
                                )

                                if response.status_code == 200:
                                    result = response.json()
                                    st.session_state.reanalyzed_score = result["score"]
                                    st.success("✅ Re-analysis complete!")
                                    st.rerun()
                                else:
                                    st.error(f"Error: {response.status_code}")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                with col2:
                    if st.button("📥 Download PDF", use_container_width=True):
                        with st.spinner("Generating PDF..."):
                            try:
                                response = requests.post(
                                    f"{BACKEND_URL}/download-resume",
                                    files={"file": data["file"]},
                                    data={"job_description": data["jd"]},
                                    timeout=60
                                )

                                if response.status_code == 200:
                                    st.download_button(
                                        label="💾 Download",
                                        data=response.content,
                                        file_name="optimized_resume.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                with col3:
                    if st.button("🔄 Generate New Version", use_container_width=True):
                        st.session_state.rewritten = None
                        st.session_state.new_score = None
                        if "reanalyzed_score" in st.session_state:
                            del st.session_state.reanalyzed_score
                        st.rerun()

                # Show re-analyzed scores if available
                if "reanalyzed_score" in st.session_state:
                    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
                    st.subheader("📊 Re-Analysis Results")

                    reanalyzed = st.session_state.reanalyzed_score

                    col1, col2, col3, col4 = st.columns(4, gap="medium")

                    with col1:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-icon'>🎯</div>
                                <div class='metric-value'>{reanalyzed['ats_score']}%</div>
                                <div class='metric-label'>ATS Score</div>
                            </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-icon'>🔤</div>
                                <div class='metric-value'>{reanalyzed['keyword_score']}%</div>
                                <div class='metric-label'>Keyword Match</div>
                            </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-icon'>🧠</div>
                                <div class='metric-value'>{reanalyzed['semantic_score']}%</div>
                                <div class='metric-label'>Content Match</div>
                            </div>
                        """, unsafe_allow_html=True)

                    with col4:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-icon'>✅</div>
                                <div class='metric-value'>{len(reanalyzed['matched_keywords'])}</div>
                                <div class='metric-label'>Keywords Found</div>
                            </div>
                        """, unsafe_allow_html=True)

                    # Comparison details
                    st.subheader("📈 Detailed Comparison")

                    comp_col1, comp_col2, comp_col3 = st.columns(3)

                    with comp_col1:
                        st.metric("ATS Score", f"{reanalyzed['ats_score']}%",
                                 delta=f"{reanalyzed['ats_score'] - score_data['ats_score']:+d}%")

                    with comp_col2:
                        st.metric("Keyword Match", f"{reanalyzed['keyword_score']}%",
                                 delta=f"{reanalyzed['keyword_score'] - score_data['keyword_score']:+d}%")

                    with comp_col3:
                        st.metric("Content Match", f"{reanalyzed['semantic_score']}%",
                                 delta=f"{reanalyzed['semantic_score'] - score_data['semantic_score']:+d}%")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
