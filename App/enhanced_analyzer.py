"""
Enhanced Resume Analyzer with Advanced AI Features
Integrates transformer models and provides intelligent resume analysis
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import numpy as np

from advanced_nlp import AdvancedNLPEngine, ResumeRewriter

class EnhancedResumeAnalyzer:
    """Enhanced resume analyzer with AI-powered features"""
    
    def __init__(self):
        self.nlp_engine = AdvancedNLPEngine()
        self.resume_rewriter = ResumeRewriter()
        
        # Industry benchmarks and salary data (simplified for demo)
        self.salary_data = {
            "data_science": {"entry": 70000, "mid": 95000, "senior": 130000, "expert": 180000},
            "web_development": {"entry": 65000, "mid": 85000, "senior": 115000, "expert": 160000},
            "mobile_development": {"entry": 70000, "mid": 90000, "senior": 125000, "expert": 170000},
            "devops": {"entry": 75000, "mid": 100000, "senior": 140000, "expert": 190000}
        }
        
        # Career progression paths
        self.career_paths = {
            "data_science": [
                "Data Analyst → Data Scientist → Senior Data Scientist → Principal Data Scientist",
                "Data Analyst → ML Engineer → Senior ML Engineer → ML Architect",
                "Data Scientist → Data Science Manager → Director of Data Science"
            ],
            "web_development": [
                "Junior Developer → Developer → Senior Developer → Tech Lead",
                "Frontend Developer → Full Stack Developer → Engineering Manager",
                "Backend Developer → System Architect → CTO"
            ]
        }
    
    def comprehensive_analysis(self, resume_text: str, resume_data: Dict) -> Dict:
        """Perform comprehensive AI-powered resume analysis"""
        analysis_results = {
            "basic_info": resume_data,
            "advanced_metrics": {},
            "ai_insights": {},
            "recommendations": {},
            "benchmarking": {},
            "career_projection": {}
        }
        
        # Advanced skill analysis
        context_aware_skills = self.nlp_engine.extract_context_aware_skills(resume_text)
        analysis_results["advanced_metrics"]["context_aware_skills"] = context_aware_skills
        
        # Experience level analysis
        experience_analysis = self.nlp_engine.analyze_experience_level(resume_text)
        analysis_results["advanced_metrics"]["experience_level"] = experience_analysis
        
        # Resume quality analysis
        quality_metrics = self.nlp_engine.analyze_resume_quality(resume_text)
        analysis_results["advanced_metrics"]["quality_metrics"] = quality_metrics
        
        # Writing quality analysis
        writing_analysis = self.resume_rewriter.analyze_writing_quality(resume_text)
        analysis_results["ai_insights"]["writing_analysis"] = writing_analysis
        
        # Determine primary field
        primary_field = self._determine_primary_field(context_aware_skills)
        analysis_results["ai_insights"]["primary_field"] = primary_field
        
        # Generate recommendations
        skill_recommendations = self.nlp_engine.generate_skill_recommendations(
            resume_data.get("skills", []), primary_field
        )
        analysis_results["recommendations"]["skills"] = skill_recommendations
        
        # Salary benchmarking
        salary_projection = self._get_salary_projection(primary_field, experience_analysis)
        analysis_results["benchmarking"]["salary_projection"] = salary_projection
        
        # Career trajectory
        career_paths = self._get_career_paths(primary_field, experience_analysis)
        analysis_results["career_projection"]["paths"] = career_paths
        
        # Generate overall score
        overall_score = self._calculate_enhanced_score(analysis_results)
        analysis_results["overall_score"] = overall_score
        
        return analysis_results
    
    def _determine_primary_field(self, skills_by_category: Dict[str, List[str]]) -> str:
        """Determine the primary field based on skill distribution"""
        skill_counts = {category: len(skills) for category, skills in skills_by_category.items()}
        
        # Field mapping
        field_mapping = {
            "programming": "software_development",
            "web_development": "web_development",
            "data_science": "data_science",
            "mobile": "mobile_development",
            "cloud": "devops"
        }
        
        max_category = max(skill_counts, key=skill_counts.get)
        return field_mapping.get(max_category, "general")
    
    def _get_salary_projection(self, field: str, experience_levels: Dict[str, float]) -> Dict:
        """Get salary projection based on field and experience"""
        if field not in self.salary_data:
            field = "web_development"  # Default fallback
        
        # Determine most likely experience level
        likely_level = max(experience_levels, key=experience_levels.get) if experience_levels else "entry"
        
        # Map experience levels to salary levels
        level_mapping = {
            "fresher": "entry",
            "junior": "entry", 
            "mid": "mid",
            "senior": "senior",
            "expert": "expert"
        }
        
        salary_level = level_mapping.get(likely_level, "entry")
        projected_salary = self.salary_data[field][salary_level]
        
        return {
            "current_level": likely_level,
            "projected_salary": projected_salary,
            "field": field,
            "salary_range": self.salary_data[field]
        }
    
    def _get_career_paths(self, field: str, experience_levels: Dict[str, float]) -> List[str]:
        """Get relevant career paths for the field"""
        return self.career_paths.get(field, ["General progression paths not available"])
    
    def _calculate_enhanced_score(self, analysis_results: Dict) -> Dict[str, float]:
        """Calculate enhanced resume score with detailed breakdown"""
        scores = {
            "content_quality": 0.0,
            "skill_relevance": 0.0,
            "experience_depth": 0.0,
            "writing_quality": 0.0,
            "completeness": 0.0
        }
        
        # Content quality (from quality metrics)
        quality_metrics = analysis_results["advanced_metrics"]["quality_metrics"]
        scores["content_quality"] = np.mean(list(quality_metrics.values()))
        
        # Skill relevance (based on context-aware skills)
        context_skills = analysis_results["advanced_metrics"]["context_aware_skills"]
        total_skills = sum(len(skills) for skills in context_skills.values())
        scores["skill_relevance"] = min(total_skills / 15, 1.0)  # Normalize to 15 skills max
        
        # Experience depth
        experience_levels = analysis_results["advanced_metrics"]["experience_level"]
        if experience_levels:
            max_exp_score = max(experience_levels.values())
            scores["experience_depth"] = max_exp_score
        
        # Writing quality (inverse of issues found)
        writing_issues = analysis_results["ai_insights"]["writing_analysis"]
        issue_count = sum(len(issues["found"]) for issues in writing_issues.values())
        scores["writing_quality"] = max(0, 1 - (issue_count / 10))
        
        # Completeness (basic sections)
        basic_info = analysis_results["basic_info"]
        completeness_items = ["name", "email", "skills", "mobile_number"]
        completed = sum(1 for item in completeness_items if basic_info.get(item))
        scores["completeness"] = completed / len(completeness_items)
        
        # Overall score (weighted average)
        weights = {
            "content_quality": 0.25,
            "skill_relevance": 0.25,
            "experience_depth": 0.20,
            "writing_quality": 0.15,
            "completeness": 0.15
        }
        
        overall = sum(scores[metric] * weights[metric] for metric in scores)
        scores["overall"] = overall
        
        return scores

class JobMatcher:
    """Intelligent job matching using semantic similarity"""
    
    def __init__(self):
        self.nlp_engine = AdvancedNLPEngine()
    
    def match_resume_to_job(self, resume_text: str, job_description: str) -> Dict:
        """Match resume to job description with detailed analysis"""
        # Calculate semantic similarity
        similarity_score = self.nlp_engine.semantic_job_matching(resume_text, job_description)
        
        # Extract skills from both texts
        resume_skills = self.nlp_engine.extract_context_aware_skills(resume_text)
        job_skills = self.nlp_engine.extract_context_aware_skills(job_description)
        
        # Find skill gaps
        skill_gaps = self._find_skill_gaps(resume_skills, job_skills)
        
        # Generate tailoring recommendations
        tailoring_suggestions = self._generate_tailoring_suggestions(
            resume_text, job_description, skill_gaps
        )
        
        return {
            "similarity_score": similarity_score,
            "skill_gaps": skill_gaps,
            "tailoring_suggestions": tailoring_suggestions,
            "match_level": self._categorize_match_level(similarity_score)
        }
    
    def _find_skill_gaps(self, resume_skills: Dict, job_skills: Dict) -> Dict:
        """Find skill gaps between resume and job requirements"""
        gaps = {}
        
        for category, job_category_skills in job_skills.items():
            resume_category_skills = resume_skills.get(category, [])
            missing_skills = [skill for skill in job_category_skills 
                            if skill not in [rs.lower() for rs in resume_category_skills]]
            if missing_skills:
                gaps[category] = missing_skills
        
        return gaps
    
    def _generate_tailoring_suggestions(self, resume_text: str, job_desc: str, 
                                      skill_gaps: Dict) -> List[str]:
        """Generate specific suggestions for tailoring resume to job"""
        suggestions = []
        
        # Skill-based suggestions
        for category, missing_skills in skill_gaps.items():
            if missing_skills:
                suggestions.append(
                    f"Add {category} skills: {', '.join(missing_skills[:3])}"
                )
        
        # Keyword optimization
        job_keywords = self._extract_important_keywords(job_desc)
        resume_keywords = self._extract_important_keywords(resume_text)
        
        missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
        if missing_keywords:
            suggestions.append(
                f"Include key terms: {', '.join(missing_keywords[:5])}"
            )
        
        return suggestions
    
    def _extract_important_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction (can be enhanced with TF-IDF)
        important_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b\w+(?:\.js|\.py|\.java)\b',  # File extensions
            r'\b\d+\+?\s*years?\b'  # Experience years
        ]
        
        keywords = []
        for pattern in important_patterns:
            keywords.extend(re.findall(pattern, text))
        
        return list(set(keywords))
    
    def _categorize_match_level(self, similarity_score: float) -> str:
        """Categorize match level based on similarity score"""
        if similarity_score >= 0.8:
            return "Excellent Match"
        elif similarity_score >= 0.6:
            return "Good Match"
        elif similarity_score >= 0.4:
            return "Fair Match"
        else:
            return "Poor Match"

class CareerPredictor:
    """Career trajectory prediction and visualization"""
    
    def __init__(self):
        self.nlp_engine = AdvancedNLPEngine()
        
        # Skill progression data
        self.skill_progressions = {
            "data_science": {
                "beginner": ["python", "sql", "excel"],
                "intermediate": ["machine learning", "pandas", "numpy", "matplotlib"],
                "advanced": ["deep learning", "tensorflow", "pytorch", "mlops"],
                "expert": ["model deployment", "distributed computing", "research"]
            }
        }
    
    def predict_career_trajectory(self, analysis_results: Dict) -> Dict:
        """Predict career trajectory based on current skills and experience"""
        current_skills = analysis_results["advanced_metrics"]["context_aware_skills"]
        experience_level = analysis_results["advanced_metrics"]["experience_level"]
        primary_field = analysis_results["ai_insights"]["primary_field"]
        
        # Determine current skill level
        skill_level = self._assess_skill_level(current_skills, primary_field)
        
        # Predict next career steps
        next_steps = self._predict_next_steps(skill_level, experience_level, primary_field)
        
        # Timeline estimation
        timeline = self._estimate_timeline(skill_level, experience_level)
        
        return {
            "current_level": skill_level,
            "next_steps": next_steps,
            "timeline": timeline,
            "growth_opportunities": self._identify_growth_opportunities(current_skills, primary_field)
        }
    
    def _assess_skill_level(self, current_skills: Dict, field: str) -> str:
        """Assess current skill level in the field"""
        if field not in self.skill_progressions:
            return "intermediate"
        
        field_skills = self.skill_progressions[field]
        skill_counts = {}
        
        # Count skills at each level
        for level, level_skills in field_skills.items():
            all_current = [skill.lower() for skills_list in current_skills.values() 
                          for skill in skills_list]
            count = sum(1 for skill in level_skills if skill in all_current)
            skill_counts[level] = count / len(level_skills)
        
        # Determine level based on highest percentage
        return max(skill_counts, key=skill_counts.get)
    
    def _predict_next_steps(self, skill_level: str, experience_level: Dict, field: str) -> List[str]:
        """Predict next career steps"""
        steps = []
        
        # Level progression
        level_progression = {
            "beginner": "intermediate",
            "intermediate": "advanced", 
            "advanced": "expert",
            "expert": "leadership"
        }
        
        next_level = level_progression.get(skill_level, "advanced")
        steps.append(f"Progress to {next_level} level skills")
        
        # Experience-based recommendations
        max_exp_level = max(experience_level, key=experience_level.get) if experience_level else "fresher"
        
        if max_exp_level in ["fresher", "junior"]:
            steps.append("Gain hands-on project experience")
            steps.append("Build a strong portfolio")
        elif max_exp_level == "mid":
            steps.append("Take on leadership responsibilities")
            steps.append("Mentor junior team members")
        else:
            steps.append("Consider strategic roles")
            steps.append("Contribute to open source projects")
        
        return steps
    
    def _estimate_timeline(self, skill_level: str, experience_level: Dict) -> Dict:
        """Estimate timeline for career progression"""
        timelines = {
            "beginner": {"next_level": "6-12 months", "senior_role": "3-5 years"},
            "intermediate": {"next_level": "12-18 months", "senior_role": "2-3 years"},
            "advanced": {"next_level": "18-24 months", "senior_role": "1-2 years"},
            "expert": {"next_level": "2-3 years", "senior_role": "Immediate"}
        }
        
        return timelines.get(skill_level, timelines["intermediate"])
    
    def _identify_growth_opportunities(self, current_skills: Dict, field: str) -> List[str]:
        """Identify specific growth opportunities"""
        opportunities = [
            "Contribute to open source projects",
            "Attend industry conferences and meetups",
            "Obtain relevant certifications",
            "Take on cross-functional projects",
            "Develop mentoring relationships"
        ]
        
        # Field-specific opportunities
        field_opportunities = {
            "data_science": [
                "Participate in Kaggle competitions",
                "Publish research papers or blog posts",
                "Learn MLOps and deployment skills"
            ],
            "web_development": [
                "Contribute to popular frameworks",
                "Build and deploy personal projects",
                "Learn emerging technologies"
            ]
        }
        
        if field in field_opportunities:
            opportunities.extend(field_opportunities[field])
        
        return opportunities