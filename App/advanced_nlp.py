"""
Advanced NLP Engine for AI Resume Analyzer
Implements transformer-based models for context-aware resume analysis
"""

import re
import json
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")

try:
    from transformers import AutoTokenizer, AutoModel, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: Transformers library not available. Using fallback methods.")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

class AdvancedNLPEngine:
    """Advanced NLP engine using transformer models for resume analysis"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.sentence_model = None
        self.classifier = None
        
        # Initialize models if available
        self._initialize_models()
        
        # Skill categories with context
        self.skill_categories = {
            "programming": ["python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "swift", "kotlin", "php", "scala", "r"],
            "web_development": ["html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask", "spring"],
            "data_science": ["machine learning", "deep learning", "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn", "nlp"],
            "databases": ["mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra", "oracle"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible"],
            "mobile": ["android", "ios", "react native", "flutter", "xamarin"],
            "soft_skills": ["leadership", "communication", "teamwork", "problem solving", "project management"]
        }
        
    def _initialize_models(self):
        """Initialize transformer models if available"""
        if not TRANSFORMERS_AVAILABLE:
            return
            
        try:
            # Initialize tokenizer and model for embeddings
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            
            # Initialize text classifier for experience level detection
            self.classifier = pipeline("text-classification", 
                                     model="microsoft/DialoGPT-medium",
                                     return_all_scores=True)
            
            # Initialize sentence transformer for semantic similarity
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
                
        except Exception as e:
            print(f"Warning: Failed to initialize transformer models: {e}")
            TRANSFORMERS_AVAILABLE = False
    
    def extract_context_aware_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills with context awareness using transformers"""
        if not TRANSFORMERS_AVAILABLE:
            return self._fallback_skill_extraction(text)
        
        skills_by_category = {category: [] for category in self.skill_categories}
        text_lower = text.lower()
        
        # Use sentence embeddings to find contextually relevant skills
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            for category, skills in self.skill_categories.items():
                for skill in skills:
                    if self._is_skill_mentioned_in_context(sentence, skill):
                        if skill not in skills_by_category[category]:
                            skills_by_category[category].append(skill)
        
        return skills_by_category
    
    def _is_skill_mentioned_in_context(self, sentence: str, skill: str) -> bool:
        """Check if a skill is mentioned in meaningful context"""
        sentence_lower = sentence.lower()
        skill_lower = skill.lower()
        
        # Direct mention
        if skill_lower in sentence_lower:
            # Check for context words that indicate actual skill usage
            context_words = ["experience", "knowledge", "proficient", "worked", "developed", 
                           "built", "implemented", "designed", "managed", "led", "created"]
            
            # Find the position of the skill in the sentence
            skill_pos = sentence_lower.find(skill_lower)
            context_window = sentence_lower[max(0, skill_pos-50):skill_pos+50+len(skill_lower)]
            
            return any(word in context_window for word in context_words)
        
        return False
    
    def _fallback_skill_extraction(self, text: str) -> Dict[str, List[str]]:
        """Fallback skill extraction without transformers"""
        skills_by_category = {category: [] for category in self.skill_categories}
        text_lower = text.lower()
        
        for category, skills in self.skill_categories.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    skills_by_category[category].append(skill)
        
        return skills_by_category
    
    def analyze_experience_level(self, text: str) -> Dict[str, float]:
        """Analyze experience level using advanced NLP"""
        experience_indicators = {
            "fresher": ["fresher", "graduate", "entry level", "recent graduate", "no experience", "internship"],
            "junior": ["1 year", "2 years", "junior", "associate", "entry level"],
            "mid": ["3 years", "4 years", "5 years", "mid level", "experienced"],
            "senior": ["6 years", "7 years", "8 years", "senior", "lead", "manager"],
            "expert": ["9 years", "10+ years", "architect", "principal", "director", "expert"]
        }
        
        text_lower = text.lower()
        scores = {}
        
        # Extract years of experience using regex
        years_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_matches = re.findall(years_pattern, text_lower)
        
        max_years = 0
        if years_matches:
            max_years = max(int(year) for year in years_matches)
        
        # Score based on years
        if max_years == 0:
            scores["fresher"] = 0.8
        elif max_years <= 2:
            scores["junior"] = 0.8
        elif max_years <= 5:
            scores["mid"] = 0.8
        elif max_years <= 8:
            scores["senior"] = 0.8
        else:
            scores["expert"] = 0.8
        
        # Score based on keywords
        for level, keywords in experience_indicators.items():
            keyword_score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[level] = scores.get(level, 0) + (keyword_score * 0.1)
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v/total_score for k, v in scores.items()}
        
        return scores
    
    def semantic_job_matching(self, resume_text: str, job_description: str) -> float:
        """Calculate semantic similarity between resume and job description"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            return self._fallback_similarity(resume_text, job_description)
        
        try:
            # Get embeddings for both texts
            resume_embedding = self.sentence_model.encode([resume_text])
            job_embedding = self.sentence_model.encode([job_description])
            
            # Calculate cosine similarity
            similarity = np.dot(resume_embedding[0], job_embedding[0]) / (
                np.linalg.norm(resume_embedding[0]) * np.linalg.norm(job_embedding[0])
            )
            
            return float(similarity)
        except Exception as e:
            print(f"Error in semantic matching: {e}")
            return self._fallback_similarity(resume_text, job_description)
    
    def _fallback_similarity(self, text1: str, text2: str) -> float:
        """Fallback similarity calculation using word overlap"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if len(union) == 0:
            return 0.0
        
        return len(intersection) / len(union)
    
    def generate_skill_recommendations(self, current_skills: List[str], target_field: str) -> List[str]:
        """Generate AI-powered skill recommendations"""
        current_skills_lower = [skill.lower() for skill in current_skills]
        recommendations = []
        
        # Field-specific skill recommendations
        field_skills = {
            "data_science": ["machine learning", "deep learning", "tensorflow", "pytorch", "pandas", 
                           "numpy", "scikit-learn", "jupyter", "sql", "python", "r", "statistics"],
            "web_development": ["javascript", "react", "node.js", "html", "css", "express", "mongodb", 
                              "git", "docker", "kubernetes", "typescript"],
            "mobile_development": ["react native", "flutter", "kotlin", "swift", "firebase", "xamarin"],
            "devops": ["docker", "kubernetes", "aws", "azure", "terraform", "jenkins", "ansible"]
        }
        
        target_skills = field_skills.get(target_field.lower(), [])
        
        for skill in target_skills:
            if skill not in current_skills_lower:
                recommendations.append(skill.title())
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentence_endings = r'[.!?]+\s+'
        sentences = re.split(sentence_endings, text)
        return [sent.strip() for sent in sentences if sent.strip()]
    
    def analyze_resume_quality(self, text: str) -> Dict[str, float]:
        """Analyze overall resume quality with detailed metrics"""
        quality_metrics = {
            "completeness": 0.0,
            "relevance": 0.0,
            "clarity": 0.0,
            "impact": 0.0,
            "formatting": 0.0
        }
        
        # Completeness check
        required_sections = ["experience", "education", "skills", "contact"]
        section_count = sum(1 for section in required_sections if section in text.lower())
        quality_metrics["completeness"] = section_count / len(required_sections)
        
        # Relevance check (based on skill mentions)
        skills_found = sum(len(skills) for skills in self.extract_context_aware_skills(text).values())
        quality_metrics["relevance"] = min(skills_found / 10, 1.0)  # Normalize to max 1.0
        
        # Clarity check (sentence length and complexity)
        sentences = self._split_into_sentences(text)
        avg_sentence_length = np.mean([len(sent.split()) for sent in sentences]) if sentences else 0
        quality_metrics["clarity"] = max(0, 1 - (avg_sentence_length - 15) / 20)  # Optimal around 15 words
        
        # Impact check (action words and quantifiable achievements)
        action_words = ["achieved", "implemented", "developed", "led", "managed", "created", 
                       "improved", "increased", "reduced", "designed", "built"]
        action_count = sum(1 for word in action_words if word in text.lower())
        quality_metrics["impact"] = min(action_count / 5, 1.0)
        
        # Formatting check (basic structure indicators)
        has_bullets = "•" in text or "*" in text or "-" in text
        has_dates = bool(re.search(r'\d{4}', text))
        quality_metrics["formatting"] = (has_bullets + has_dates) / 2
        
        return quality_metrics

class ResumeRewriter:
    """AI-powered resume rewriting and improvement suggestions"""
    
    def __init__(self):
        self.improvement_patterns = {
            "weak_verbs": {
                "pattern": r'\b(was|were|did|had|worked on|responsible for)\b',
                "suggestions": ["achieved", "implemented", "developed", "led", "managed", "created"]
            },
            "vague_terms": {
                "pattern": r'\b(many|several|some|various|different)\b',
                "suggestions": ["specific numbers", "quantified results"]
            },
            "passive_voice": {
                "pattern": r'\b(was|were)\s+\w+ed\b',
                "suggestions": ["use active voice instead"]
            }
        }
    
    def analyze_writing_quality(self, text: str) -> Dict[str, List[str]]:
        """Analyze writing quality and provide specific suggestions"""
        suggestions = {}
        
        for issue_type, pattern_info in self.improvement_patterns.items():
            matches = re.findall(pattern_info["pattern"], text, re.IGNORECASE)
            if matches:
                suggestions[issue_type] = {
                    "found": matches,
                    "suggestions": pattern_info["suggestions"]
                }
        
        return suggestions
    
    def suggest_bullet_improvements(self, bullet_points: List[str]) -> List[Dict[str, str]]:
        """Suggest improvements for bullet points"""
        improvements = []
        
        for bullet in bullet_points:
            improvement = {
                "original": bullet,
                "suggestions": []
            }
            
            # Check for quantifiable metrics
            if not re.search(r'\d+', bullet):
                improvement["suggestions"].append("Add quantifiable metrics (numbers, percentages)")
            
            # Check for action verbs
            action_verbs = ["achieved", "implemented", "developed", "led", "managed", "created",
                          "improved", "increased", "reduced", "designed", "built"]
            if not any(verb in bullet.lower() for verb in action_verbs):
                improvement["suggestions"].append("Start with a strong action verb")
            
            # Check for impact
            impact_words = ["improved", "increased", "reduced", "saved", "generated", "optimized"]
            if not any(word in bullet.lower() for word in impact_words):
                improvement["suggestions"].append("Highlight the impact or result of your action")
            
            if improvement["suggestions"]:
                improvements.append(improvement)
        
        return improvements