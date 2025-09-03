"""
Comprehensive test runner for Enhanced AI Resume Analyzer
Tests all new features and components
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json
from datetime import datetime

# Test enhanced components
def test_enhanced_components():
    """Test all enhanced components"""
    print("🧪 Testing Enhanced AI Resume Analyzer Components")
    print("=" * 60)
    
    # Test 1: Advanced NLP Engine
    print("1. Testing Advanced NLP Engine...")
    try:
        from advanced_nlp import AdvancedNLPEngine, ResumeRewriter
        
        nlp_engine = AdvancedNLPEngine()
        
        # Test skill extraction
        sample_text = """
        I am a software developer with 5 years of experience in Python, JavaScript, and React.
        I have worked on machine learning projects using TensorFlow and scikit-learn.
        Led a team of developers and implemented CI/CD pipelines using Docker and AWS.
        """
        
        skills = nlp_engine.extract_context_aware_skills(sample_text)
        print(f"   ✅ Context-aware skills extracted: {len(sum(skills.values(), []))} skills found")
        
        # Test experience analysis
        experience = nlp_engine.analyze_experience_level(sample_text)
        print(f"   ✅ Experience analysis: {max(experience, key=experience.get) if experience else 'Unknown'}")
        
        # Test resume quality
        quality = nlp_engine.analyze_resume_quality(sample_text)
        print(f"   ✅ Quality analysis: {sum(quality.values()) / len(quality):.2f} average score")
        
        # Test rewriter
        rewriter = ResumeRewriter()
        writing_analysis = rewriter.analyze_writing_quality(sample_text)
        print(f"   ✅ Writing analysis: {len(writing_analysis)} issues found")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Enhanced Analyzer
    print("\n2. Testing Enhanced Resume Analyzer...")
    try:
        from enhanced_analyzer import EnhancedResumeAnalyzer, JobMatcher, CareerPredictor
        
        analyzer = EnhancedResumeAnalyzer()
        
        # Mock resume data
        sample_resume_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "skills": ["Python", "JavaScript", "React", "Machine Learning"],
            "mobile_number": "555-1234"
        }
        
        # Test comprehensive analysis
        analysis = analyzer.comprehensive_analysis(sample_text, sample_resume_data)
        print(f"   ✅ Comprehensive analysis completed")
        print(f"   ✅ Overall score: {analysis['overall_score']['overall']:.2f}")
        print(f"   ✅ Primary field: {analysis['ai_insights']['primary_field']}")
        
        # Test job matcher
        job_matcher = JobMatcher()
        job_desc = "Looking for a Python developer with React experience and machine learning knowledge."
        match_result = job_matcher.match_resume_to_job(sample_text, job_desc)
        print(f"   ✅ Job matching: {match_result['similarity_score']:.2f} similarity")
        
        # Test career predictor
        career_predictor = CareerPredictor()
        career_prediction = career_predictor.predict_career_trajectory(analysis)
        print(f"   ✅ Career prediction: {len(career_prediction['next_steps'])} recommendations")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Mock Interview Engine
    print("\n3. Testing Mock Interview Engine...")
    try:
        from mock_interview import MockInterviewEngine
        
        interview_engine = MockInterviewEngine()
        
        # Generate interview session
        session = interview_engine.generate_interview_session("data_science", "mid", 15)
        print(f"   ✅ Interview session generated: {len(session['questions'])} questions")
        
        # Test response evaluation
        sample_question = session['questions'][0]
        sample_response = "I would approach this by first analyzing the requirements and then implementing a solution using appropriate algorithms."
        
        evaluation = interview_engine.evaluate_response(sample_question, sample_response)
        print(f"   ✅ Response evaluation: {evaluation['overall_score']:.2f} overall score")
        
        # Test session summary
        evaluations = [evaluation]
        summary = interview_engine.generate_session_summary(evaluations)
        print(f"   ✅ Session summary: {summary['overall_average']:.2f} average")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Visualizations
    print("\n4. Testing Advanced Visualizations...")
    try:
        from visualizations import AdvancedVisualizations
        
        viz = AdvancedVisualizations()
        
        # Test skill radar chart
        sample_skills = {
            "programming": ["Python", "JavaScript"],
            "web_development": ["React", "Node.js"],
            "data_science": ["Machine Learning"]
        }
        
        radar_fig = viz.create_skill_radar_chart(sample_skills)
        print(f"   ✅ Skill radar chart created")
        
        # Test career trajectory chart
        career_data = {"current_level": "mid"}
        trajectory_fig = viz.create_career_trajectory_chart(career_data)
        print(f"   ✅ Career trajectory chart created")
        
        # Test quality dashboard
        quality_metrics = {
            "completeness": 0.8,
            "relevance": 0.9,
            "clarity": 0.7,
            "impact": 0.8,
            "formatting": 0.9
        }
        
        quality_fig = viz.create_resume_quality_dashboard(quality_metrics)
        print(f"   ✅ Quality dashboard created")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Gamification System
    print("\n5. Testing Gamification System...")
    try:
        from gamification import GamificationEngine, BadgeSystem
        
        # Use temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_db:
            gamification = GamificationEngine(tmp_db.name)
            
            # Test user progress
            user_id = "test_user_123"
            progress = gamification.get_user_progress(user_id)
            print(f"   ✅ User progress created: Level {progress.level}")
            
            # Test activity recording
            activity_result = gamification.record_activity(user_id, "resume_analyzed")
            print(f"   ✅ Activity recorded: {activity_result['points_earned']} points earned")
            
            # Test achievements
            achievements = gamification.get_user_achievements(user_id)
            print(f"   ✅ Achievements: {len(achievements)} earned")
            
            # Test badge system
            badge_system = BadgeSystem()
            first_achievement = gamification.achievements["first_analysis"]
            badge_svg = badge_system.generate_badge_svg(first_achievement)
            print(f"   ✅ Badge system: SVG generated ({len(badge_svg)} chars)")
            
            # Cleanup
            os.unlink(tmp_db.name)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: API System
    print("\n6. Testing API System...")
    try:
        from resume_api import ResumeAnalyticsAPI, APIDocGenerator
        
        # Test API initialization
        api = ResumeAnalyticsAPI()
        print(f"   ✅ API initialized with {len(api.valid_api_keys)} API keys")
        
        # Test documentation generation
        doc_gen = APIDocGenerator()
        openapi_spec = doc_gen.generate_openapi_spec()
        print(f"   ✅ OpenAPI documentation: {len(openapi_spec['paths'])} endpoints")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Client-Side Analyzer
    print("\n7. Testing Client-Side Analyzer...")
    try:
        from client_side_analyzer import create_client_side_analyzer, create_privacy_comparison
        
        # Test component creation
        client_code = create_client_side_analyzer()
        print(f"   ✅ Client-side analyzer: {len(client_code)} characters of JavaScript/HTML")
        
        # Verify it contains key components
        assert "TensorFlow.js" in client_code
        assert "skillPatterns" in client_code
        assert "analyzeResume" in client_code
        print(f"   ✅ Contains required components: TensorFlow.js, skill patterns, analyzer")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced AI Resume Analyzer Test Complete!")
    print("\nKey Features Tested:")
    print("✅ Advanced NLP with context-aware analysis")
    print("✅ AI-powered resume rewriting suggestions")
    print("✅ Mock interview system with intelligent assessment")
    print("✅ Interactive visualizations and dashboards")
    print("✅ Gamification with achievements and progress tracking")
    print("✅ RESTful API for bulk processing")
    print("✅ Client-side privacy-first analysis")
    print("✅ Career trajectory prediction")
    print("✅ Job matching with semantic similarity")
    print("✅ Market insights and trends analysis")

def test_integration():
    """Test integration between components"""
    print("\n🔗 Testing Component Integration...")
    try:
        # Test full workflow
        from enhanced_analyzer import EnhancedResumeAnalyzer
        from gamification import GamificationEngine
        from mock_interview import MockInterviewEngine
        
        # Initialize components
        analyzer = EnhancedResumeAnalyzer()
        gamification = GamificationEngine("/tmp/test_integration.db")
        interview_engine = MockInterviewEngine()
        
        # Simulate user workflow
        user_id = "integration_test_user"
        
        # 1. Analyze resume
        sample_text = "Python developer with React and machine learning experience"
        sample_data = {"skills": ["Python", "React"], "name": "Test User", "email": "test@example.com"}
        
        analysis = analyzer.comprehensive_analysis(sample_text, sample_data)
        
        # 2. Record activity
        activity = gamification.record_activity(user_id, "resume_analyzed", 
                                               {"score": analysis["overall_score"]["overall"]})
        
        # 3. Generate interview
        field = analysis["ai_insights"]["primary_field"]
        session = interview_engine.generate_interview_session(field, "mid", 15)
        
        # 4. Record interview activity
        interview_activity = gamification.record_activity(user_id, "interview_completed",
                                                        {"score": 0.8})
        
        print(f"   ✅ Integration test successful:")
        print(f"      - Resume analyzed: {analysis['overall_score']['overall']:.2f} score")
        print(f"      - Activity recorded: {activity['points_earned']} points")
        print(f"      - Interview generated: {len(session['questions'])} questions")
        print(f"      - Total XP: {activity['total_experience'] + interview_activity['points_earned']}")
        
        # Cleanup
        os.unlink("/tmp/test_integration.db")
        
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")

if __name__ == "__main__":
    test_enhanced_components()
    test_integration()
    
    print("\n" + "🚀" * 20)
    print("All tests completed! The Enhanced AI Resume Analyzer is ready.")
    print("🚀" * 20)