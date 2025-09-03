"""
Enhanced AI Resume Analyzer - Main Application
Integrates advanced AI features, gamification, and interactive dashboards
"""

import streamlit as st
import pandas as pd
import base64
import time
import datetime
import pymysql
import os
import socket
import platform
import geocoder
import secrets
import io
import random
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

# Import enhanced modules
try:
    from enhanced_analyzer import EnhancedResumeAnalyzer, JobMatcher, CareerPredictor
    from mock_interview import MockInterviewEngine
    from visualizations import AdvancedVisualizations, create_gamification_dashboard
    from gamification import GamificationEngine, BadgeSystem, GAMIFICATION_CSS
    from advanced_nlp import AdvancedNLPEngine, ResumeRewriter
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError as e:
    print(f"Enhanced features not available: {e}")
    ENHANCED_FEATURES_AVAILABLE = False

# Import original modules
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from streamlit_tags import st_tags
from Courses import ds_course, web_course, android_course, ios_course, uiux_course
from Courses import resume_videos, interview_videos
import nltk
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Initialize enhanced components
if ENHANCED_FEATURES_AVAILABLE:
    enhanced_analyzer = EnhancedResumeAnalyzer()
    job_matcher = JobMatcher()
    career_predictor = CareerPredictor()
    interview_engine = MockInterviewEngine()
    visualizations = AdvancedVisualizations()
    gamification_engine = GamificationEngine()
    badge_system = BadgeSystem()

# Original helper functions
def get_csv_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        
        text = fake_file_handle.getvalue()
    
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def course_recommender(course_list):
    st.subheader("**Courses & Certificates🎓 Recommendations**")
    c = 0
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course

# Database configuration (simplified for demo)
try:
    connection = pymysql.connect(host='localhost', user='root', password='', db='cv_enhanced')
    cursor = connection.cursor()
except:
    # Use SQLite as fallback
    import sqlite3
    connection = sqlite3.connect('/tmp/cv_enhanced.db')
    cursor = connection.cursor()

# Page configuration
st.set_page_config(
    page_title="Enhanced AI Resume Analyzer",
    page_icon='🚀',
    layout="wide"
)

def run():
    # Custom CSS for enhanced UI
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add gamification CSS
    if ENHANCED_FEATURES_AVAILABLE:
        st.markdown(GAMIFICATION_CSS, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Enhanced AI Resume Analyzer</h1>
        <p>Advanced AI-powered resume analysis with personalized insights and career guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("# Choose Your Path...")
    
    if ENHANCED_FEATURES_AVAILABLE:
        activities = [
            "🎯 Smart Analysis", 
            "🎤 Mock Interview", 
            "📊 Career Insights",
            "🎮 Your Progress",
            "💼 Job Matching",
            "📈 Market Insights",
            "💬 Feedback", 
            "ℹ️ About", 
            "👨‍💼 Admin"
        ]
    else:
        activities = ["User", "Feedback", "About", "Admin"]
    
    choice = st.sidebar.selectbox("Choose among the options:", activities)
    
    # User session management
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{random.randint(1000, 9999)}"
    
    # Main application logic
    if choice == "🎯 Smart Analysis":
        smart_analysis_page()
    elif choice == "🎤 Mock Interview":
        mock_interview_page()
    elif choice == "📊 Career Insights":
        career_insights_page()
    elif choice == "🎮 Your Progress":
        progress_page()
    elif choice == "💼 Job Matching":
        job_matching_page()
    elif choice == "📈 Market Insights":
        market_insights_page()
    elif choice == "💬 Feedback":
        feedback_page()
    elif choice == "ℹ️ About":
        about_page()
    elif choice == "👨‍💼 Admin":
        admin_page()
    else:
        # Fallback to original user page
        original_user_page()

def smart_analysis_page():
    """Enhanced smart analysis page with AI features"""
    st.header("🎯 Smart Resume Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Your Resume")
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        
        if pdf_file is not None:
            # Save uploaded file
            save_path = f"/tmp/{pdf_file.name}"
            with open(save_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            
            # Show PDF
            show_pdf(save_path)
            
            # Process with enhanced analyzer
            if ENHANCED_FEATURES_AVAILABLE:
                process_resume_enhanced(save_path, pdf_file.name)
            else:
                st.warning("Enhanced features not available. Using basic analysis.")
                process_resume_basic(save_path)
    
    with col2:
        st.subheader("📈 Quick Stats")
        if ENHANCED_FEATURES_AVAILABLE:
            display_quick_stats()

def process_resume_enhanced(file_path, filename):
    """Process resume with enhanced AI features"""
    with st.spinner("🤖 Analyzing your resume with AI..."):
        try:
            # Parse resume
            parser = ResumeParser(file_path)
            basic_data = parser.get_extracted_data()
            
            # Extract text
            resume_text = pdf_reader(file_path)
            
            # Enhanced analysis
            analysis_result = enhanced_analyzer.comprehensive_analysis(resume_text, basic_data)
            
            # Record activity for gamification
            activity_result = gamification_engine.record_activity(
                st.session_state.user_id, 
                "resume_analyzed",
                {"filename": filename}
            )
            
            # Display results
            display_analysis_results(analysis_result, activity_result)
            
        except Exception as e:
            st.error(f"Error analyzing resume: {str(e)}")

def display_analysis_results(analysis_result, activity_result):
    """Display comprehensive analysis results"""
    
    # Show gamification feedback
    if activity_result.get("level_up"):
        st.balloons()
        st.success(f"🎉 Level Up! You're now level {activity_result['new_level']}!")
    
    if activity_result.get("new_achievements"):
        for achievement_id in activity_result["new_achievements"]:
            achievement = gamification_engine.achievements[achievement_id]
            st.success(f"🏆 Achievement Unlocked: {achievement.name}!")
    
    # Tabs for different analysis views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "🎯 Skills Analysis", "📈 Quality Metrics", 
        "💡 AI Recommendations", "🚀 Career Path"
    ])
    
    with tab1:
        display_overview_tab(analysis_result)
    
    with tab2:
        display_skills_tab(analysis_result)
    
    with tab3:
        display_quality_tab(analysis_result)
    
    with tab4:
        display_recommendations_tab(analysis_result)
    
    with tab5:
        display_career_tab(analysis_result)

def display_overview_tab(analysis_result):
    """Display overview tab with key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    overall_score = analysis_result["overall_score"]["overall"]
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{overall_score:.0%}</h3>
            <p>Overall Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        primary_field = analysis_result["ai_insights"]["primary_field"]
        st.markdown(f"""
        <div class="metric-card">
            <h3>{primary_field.replace('_', ' ').title()}</h3>
            <p>Predicted Field</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        exp_levels = analysis_result["advanced_metrics"]["experience_level"]
        likely_level = max(exp_levels, key=exp_levels.get) if exp_levels else "Entry"
        st.markdown(f"""
        <div class="metric-card">
            <h3>{likely_level.title()}</h3>
            <p>Experience Level</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        salary_projection = analysis_result["benchmarking"]["salary_projection"]
        projected_salary = salary_projection.get("projected_salary", 0)
        st.markdown(f"""
        <div class="metric-card">
            <h3>${projected_salary:,}</h3>
            <p>Projected Salary</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quality dashboard
    st.subheader("📊 Resume Quality Dashboard")
    quality_metrics = analysis_result["advanced_metrics"]["quality_metrics"]
    fig = visualizations.create_resume_quality_dashboard(quality_metrics)
    st.plotly_chart(fig, use_container_width=True)

def display_skills_tab(analysis_result):
    """Display skills analysis tab"""
    st.subheader("🎯 Advanced Skills Analysis")
    
    # Context-aware skills
    context_skills = analysis_result["advanced_metrics"]["context_aware_skills"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Skills by Category")
        for category, skills in context_skills.items():
            if skills:
                st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(skills)}")
    
    with col2:
        # Skills radar chart
        fig = visualizations.create_skill_radar_chart(context_skills)
        st.plotly_chart(fig, use_container_width=True)
    
    # Skill recommendations
    st.subheader("💡 Skill Recommendations")
    recommendations = analysis_result["recommendations"]["skills"]
    if recommendations:
        for skill in recommendations:
            st.write(f"• {skill}")
    else:
        st.info("Great! Your skills are comprehensive for your field.")

def display_quality_tab(analysis_result):
    """Display quality metrics tab"""
    st.subheader("📈 Writing Quality Analysis")
    
    writing_analysis = analysis_result["ai_insights"]["writing_analysis"]
    
    if writing_analysis:
        for issue_type, issue_data in writing_analysis.items():
            st.warning(f"**{issue_type.replace('_', ' ').title()}:** {len(issue_data['found'])} instances found")
            st.write(f"Suggestions: {', '.join(issue_data['suggestions'])}")
    else:
        st.success("✅ Great! No major writing issues detected.")
    
    # Quality breakdown
    quality_metrics = analysis_result["advanced_metrics"]["quality_metrics"]
    
    col1, col2 = st.columns(2)
    with col1:
        for metric, score in quality_metrics.items():
            st.metric(
                label=metric.replace('_', ' ').title(),
                value=f"{score:.1%}",
                delta=f"{(score - 0.7):.1%}" if score != 0.7 else None
            )

def display_recommendations_tab(analysis_result):
    """Display AI recommendations tab"""
    st.subheader("💡 AI-Powered Recommendations")
    
    # Resume rewriter suggestions
    if ENHANCED_FEATURES_AVAILABLE:
        rewriter = ResumeRewriter()
        # This would analyze actual resume text in real implementation
        st.write("**Writing Improvements:**")
        st.write("• Use more action verbs to start bullet points")
        st.write("• Add quantifiable metrics to your achievements")
        st.write("• Consider using active voice instead of passive voice")
    
    # Course recommendations based on field
    primary_field = analysis_result["ai_insights"]["primary_field"]
    st.subheader("📚 Recommended Courses")
    
    if primary_field == "data_science":
        course_recommender(ds_course)
    elif primary_field == "web_development":
        course_recommender(web_course)
    else:
        st.info("General skill development courses recommended.")

def display_career_tab(analysis_result):
    """Display career trajectory tab"""
    st.subheader("🚀 Career Trajectory Prediction")
    
    if ENHANCED_FEATURES_AVAILABLE:
        career_prediction = career_predictor.predict_career_trajectory(analysis_result)
        
        # Career path visualization
        career_data = {"current_level": career_prediction["current_level"]}
        fig = visualizations.create_career_trajectory_chart(career_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Next steps
        st.subheader("🎯 Recommended Next Steps")
        for step in career_prediction["next_steps"]:
            st.write(f"• {step}")
        
        # Timeline
        timeline = career_prediction["timeline"]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Next Level", timeline["next_level"])
        with col2:
            st.metric("Senior Role", timeline["senior_role"])

def mock_interview_page():
    """Mock interview page with AI assessment"""
    st.header("🎤 AI-Powered Mock Interview")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.warning("Enhanced interview features not available.")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Interview Setup")
        
        field = st.selectbox("Select Field:", [
            "data_science", "web_development", "mobile_development", "general"
        ])
        
        experience_level = st.selectbox("Experience Level:", [
            "fresher", "junior", "mid", "senior", "expert"
        ])
        
        duration = st.slider("Interview Duration (minutes):", 10, 60, 30)
        
        if st.button("🎬 Start Interview Session"):
            session = interview_engine.generate_interview_session(
                field, experience_level, duration
            )
            st.session_state.interview_session = session
            st.success("Interview session generated! Start answering questions below.")
    
    with col2:
        st.subheader("📊 Your Interview Stats")
        # Show interview history and performance
        if 'interview_history' not in st.session_state:
            st.session_state.interview_history = []
        
        if st.session_state.interview_history:
            fig = visualizations.create_interview_performance_chart(
                st.session_state.interview_history
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Complete interviews to see your performance trends.")
    
    # Interview questions
    if 'interview_session' in st.session_state:
        conduct_interview()

def conduct_interview():
    """Conduct the interview session"""
    session = st.session_state.interview_session
    
    if 'current_question_idx' not in st.session_state:
        st.session_state.current_question_idx = 0
        st.session_state.interview_responses = []
    
    current_idx = st.session_state.current_question_idx
    
    if current_idx < len(session["questions"]):
        question = session["questions"][current_idx]
        
        st.subheader(f"Question {current_idx + 1} of {len(session['questions'])}")
        st.markdown(f"**{question['type'].title()} Question:**")
        st.markdown(f"*{question['question']}*")
        
        # Response input
        response = st.text_area("Your Answer:", height=150, key=f"response_{current_idx}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⏭️ Next Question") and response.strip():
                # Evaluate response
                evaluation = interview_engine.evaluate_response(question, response)
                st.session_state.interview_responses.append(evaluation)
                st.session_state.current_question_idx += 1
                st.rerun()
        
        with col2:
            if st.button("⏭️ Skip Question"):
                st.session_state.current_question_idx += 1
                st.rerun()
        
        with col3:
            if st.button("🔚 End Interview"):
                complete_interview()
    else:
        complete_interview()

def complete_interview():
    """Complete the interview and show results"""
    if 'interview_responses' in st.session_state and st.session_state.interview_responses:
        st.success("🎉 Interview Complete!")
        
        # Generate summary
        summary = interview_engine.generate_session_summary(st.session_state.interview_responses)
        
        # Record activity
        activity_result = gamification_engine.record_activity(
            st.session_state.user_id,
            "interview_completed",
            {"score": summary["overall_average"]}
        )
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Your Performance")
            st.metric("Overall Score", f"{summary['overall_average']:.1%}")
            
            for criterion, avg_score in summary["criterion_averages"].items():
                st.metric(
                    criterion.replace('_', ' ').title(),
                    f"{avg_score:.1%}"
                )
        
        with col2:
            st.subheader("💡 Recommendations")
            for rec in summary["recommendations"]:
                st.write(f"• {rec}")
        
        # Save to history
        st.session_state.interview_history.append(summary)
        
        # Reset session
        if st.button("🔄 Start New Interview"):
            for key in ['interview_session', 'current_question_idx', 'interview_responses']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

def career_insights_page():
    """Career insights and market analysis page"""
    st.header("📊 Career Insights & Market Analysis")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.warning("Enhanced career insights not available.")
        return
    
    # Field selection
    field = st.selectbox("Select Field for Analysis:", [
        "data_science", "web_development", "mobile_development", "devops"
    ])
    
    # Market insights visualization
    fig = visualizations.create_market_insights_chart(field)
    st.plotly_chart(fig, use_container_width=True)
    
    # Networking opportunities
    st.subheader("🤝 Networking Opportunities")
    location_data = {"city": "San Francisco", "state": "CA"}  # Example
    networking_fig = visualizations.create_networking_opportunities_map(location_data)
    st.plotly_chart(networking_fig, use_container_width=True)

def progress_page():
    """User progress and gamification page"""
    st.header("🎮 Your Progress & Achievements")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.warning("Progress tracking not available.")
        return
    
    # Get user progress
    progress = gamification_engine.get_user_progress(st.session_state.user_id)
    
    # Progress dashboard
    fig = create_gamification_dashboard(progress.__dict__)
    st.plotly_chart(fig, use_container_width=True)
    
    # Achievements
    st.subheader("🏆 Your Achievements")
    earned_achievements = gamification_engine.get_user_achievements(st.session_state.user_id)
    
    if earned_achievements:
        for achievement in earned_achievements:
            badge_html = badge_system.create_achievement_card(achievement)
            st.markdown(badge_html, unsafe_allow_html=True)
    else:
        st.info("Complete activities to earn achievements!")
    
    # Achievement progress
    st.subheader("🎯 Progress Towards New Achievements")
    achievement_progress = gamification_engine.get_achievement_progress(st.session_state.user_id)
    
    for achievement_id, progress_data in list(achievement_progress.items())[:5]:  # Show top 5
        achievement = progress_data["achievement"]
        progress_pct = progress_data["overall_progress"]
        
        st.write(f"**{achievement['name']}** - {progress_pct:.0%} complete")
        st.progress(progress_pct)

def job_matching_page():
    """Job matching and resume tailoring page"""
    st.header("💼 Job Matching & Resume Tailoring")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.warning("Job matching features not available.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Your Resume")
        resume_text = st.text_area("Paste your resume text:", height=300)
    
    with col2:
        st.subheader("💼 Job Description")
        job_description = st.text_area("Paste job description:", height=300)
    
    if st.button("🔍 Analyze Match") and resume_text and job_description:
        with st.spinner("Analyzing job match..."):
            match_result = job_matcher.match_resume_to_job(resume_text, job_description)
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Match Score", f"{match_result['similarity_score']:.1%}")
                st.write(f"**Match Level:** {match_result['match_level']}")
            
            with col2:
                st.subheader("🎯 Skill Gaps")
                for category, missing_skills in match_result["skill_gaps"].items():
                    if missing_skills:
                        st.write(f"**{category.title()}:** {', '.join(missing_skills)}")
            
            # Tailoring suggestions
            st.subheader("💡 Resume Tailoring Suggestions")
            for suggestion in match_result["tailoring_suggestions"]:
                st.write(f"• {suggestion}")

def market_insights_page():
    """Market insights and trends page"""
    st.header("📈 Market Insights & Trends")
    
    if not ENHANCED_FEATURES_AVAILABLE:
        st.warning("Market insights not available.")
        return
    
    # This would integrate with real market data APIs
    st.info("🚧 Market insights integration coming soon! This will provide real-time job market data, salary trends, and skill demand analysis.")

def feedback_page():
    """Enhanced feedback page"""
    st.header("💬 Share Your Feedback")
    
    # Feedback form (simplified)
    name = st.text_input("Your Name:")
    email = st.text_input("Your Email:")
    rating = st.slider("Rate your experience:", 1, 5, 5)
    comments = st.text_area("Your feedback:")
    
    if st.button("Submit Feedback") and name and email:
        # Record feedback activity
        if ENHANCED_FEATURES_AVAILABLE:
            gamification_engine.record_activity(
                st.session_state.user_id,
                "feedback_given",
                {"rating": rating}
            )
        
        st.success("Thank you for your feedback!")

def about_page():
    """Enhanced about page"""
    st.header("ℹ️ About Enhanced AI Resume Analyzer")
    
    st.markdown("""
    ## 🚀 Welcome to the Future of Resume Analysis
    
    Our Enhanced AI Resume Analyzer goes beyond traditional keyword matching to provide:
    
    ### ✨ Advanced Features
    - **🤖 AI-Powered Analysis:** Context-aware skill detection using transformer models
    - **🎤 Mock Interviews:** Practice with role-specific questions and AI feedback
    - **📊 Career Insights:** Predict your career trajectory and salary potential
    - **🎮 Gamification:** Earn badges and track your progress
    - **💼 Job Matching:** Semantic similarity matching with job descriptions
    - **📈 Market Analytics:** Real-time insights into job market trends
    
    ### 🛠️ Technology Stack
    - **Backend:** Python, Streamlit, Advanced NLP models
    - **AI/ML:** Transformers, BERT, Sentence-BERT
    - **Database:** MySQL/SQLite with intelligent caching
    - **Visualization:** Plotly for interactive charts and dashboards
    - **APIs:** RESTful APIs for bulk processing
    
    ### 🎯 Our Mission
    To democratize career advancement through AI-powered insights and personalized guidance.
    """)

def admin_page():
    """Enhanced admin dashboard"""
    st.header("👨‍💼 Admin Dashboard")
    
    # Admin authentication (simplified)
    password = st.text_input("Admin Password:", type="password")
    
    if password != "admin123":
        st.warning("Please enter admin password to access dashboard.")
        return
    
    # Admin analytics
    st.subheader("📊 Platform Analytics")
    
    # Mock data for demonstration
    analytics_data = {
        "Total Users": 1234,
        "Resumes Analyzed": 5678,
        "Interviews Completed": 890,
        "API Requests": 12345
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    for i, (metric, value) in enumerate(analytics_data.items()):
        with [col1, col2, col3, col4][i]:
            st.metric(metric, value)
    
    # User engagement metrics
    if ENHANCED_FEATURES_AVAILABLE:
        leaderboard = gamification_engine.get_leaderboard("experience", 10)
        if leaderboard:
            st.subheader("🏆 Top Users by Experience")
            df = pd.DataFrame(leaderboard)
            st.dataframe(df)

def original_user_page():
    """Original user page as fallback"""
    st.subheader("**Original Resume Analysis**")
    st.write("Upload your resume to get basic analysis and recommendations.")
    
    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
    if pdf_file is not None:
        save_path = f"/tmp/{pdf_file.name}"
        with open(save_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        
        show_pdf(save_path)
        
        if st.button("Analyze Resume"):
            process_resume_basic(save_path)

def process_resume_basic(file_path):
    """Basic resume processing without enhanced features"""
    try:
        parser = ResumeParser(file_path)
        data = parser.get_extracted_data()
        
        st.success("Resume processed successfully!")
        st.json(data)
        
    except Exception as e:
        st.error(f"Error processing resume: {str(e)}")

def display_quick_stats():
    """Display quick statistics for the sidebar"""
    if ENHANCED_FEATURES_AVAILABLE:
        progress = gamification_engine.get_user_progress(st.session_state.user_id)
        
        st.metric("Your Level", progress.level)
        st.metric("Experience Points", progress.experience_points)
        st.metric("Resumes Analyzed", progress.total_resumes_analyzed)
        st.metric("Current Streak", f"{progress.current_streak} days")

if __name__ == '__main__':
    run()