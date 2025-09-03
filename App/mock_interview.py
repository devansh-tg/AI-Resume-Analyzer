"""
Mock Interview Module with AI-Powered Assessment
Generates role-specific questions and provides feedback
"""

import json
import random
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings("ignore")

class MockInterviewEngine:
    """AI-powered mock interview system"""
    
    def __init__(self):
        # Question bank organized by field and difficulty
        self.question_bank = {
            "data_science": {
                "technical": [
                    "Explain the difference between supervised and unsupervised learning.",
                    "How would you handle missing data in a dataset?",
                    "What is overfitting and how can you prevent it?",
                    "Describe the bias-variance tradeoff.",
                    "How do you evaluate the performance of a regression model?",
                    "What is cross-validation and why is it important?",
                    "Explain the concept of feature engineering.",
                    "What are the assumptions of linear regression?"
                ],
                "behavioral": [
                    "Tell me about a challenging data science project you worked on.",
                    "How do you communicate complex technical findings to non-technical stakeholders?",
                    "Describe a time when your initial hypothesis was wrong. How did you handle it?",
                    "How do you stay updated with the latest developments in data science?"
                ],
                "scenario": [
                    "You're given a dataset with 1 million rows and 100 columns. Walk me through your initial analysis approach.",
                    "A model you deployed is performing poorly in production. How would you debug this?",
                    "You need to present findings to executives who want immediate actionable insights. How do you approach this?"
                ]
            },
            "web_development": {
                "technical": [
                    "Explain the difference between synchronous and asynchronous JavaScript.",
                    "What is the DOM and how do you manipulate it?",
                    "Describe the concept of RESTful APIs.",
                    "What are closures in JavaScript?",
                    "Explain the difference between == and === in JavaScript.",
                    "What is the purpose of middleware in Express.js?",
                    "How does React's virtual DOM work?",
                    "What are the advantages of using a CSS preprocessor?"
                ],
                "behavioral": [
                    "Tell me about a web application you built from scratch.",
                    "How do you approach debugging a complex web application?",
                    "Describe a time when you had to optimize application performance.",
                    "How do you ensure your web applications are accessible?"
                ],
                "scenario": [
                    "A user reports that the application is slow. How would you investigate and resolve this?",
                    "You need to integrate a third-party API with rate limiting. How do you handle this?",
                    "Design a simple e-commerce checkout flow. What considerations would you make?"
                ]
            },
            "general": {
                "behavioral": [
                    "Tell me about yourself.",
                    "Why are you interested in this position?",
                    "Describe a challenging project you worked on.",
                    "How do you handle working under pressure?",
                    "Where do you see yourself in 5 years?",
                    "Tell me about a time you had to learn something new quickly.",
                    "How do you handle conflicts with team members?",
                    "What motivates you in your work?"
                ],
                "scenario": [
                    "You're given a project with a tight deadline. How do you prioritize tasks?",
                    "A stakeholder requests a feature that you think is technically unfeasible. How do you handle this?",
                    "You discover a critical bug in production. Walk me through your response."
                ]
            }
        }
        
        # Evaluation criteria
        self.evaluation_criteria = {
            "technical_accuracy": {
                "weight": 0.3,
                "description": "Correctness and depth of technical knowledge"
            },
            "communication": {
                "weight": 0.25,
                "description": "Clarity and effectiveness of communication"
            },
            "problem_solving": {
                "weight": 0.25,
                "description": "Approach to solving problems and thinking process"
            },
            "confidence": {
                "weight": 0.1,
                "description": "Confidence and composure during responses"
            },
            "examples": {
                "weight": 0.1,
                "description": "Use of relevant examples and experiences"
            }
        }
    
    def generate_interview_session(self, field: str, experience_level: str, 
                                 duration_minutes: int = 30) -> Dict:
        """Generate a complete interview session"""
        # Determine number of questions based on duration
        questions_per_minute = 0.5  # Approximately 2 minutes per question
        total_questions = int(duration_minutes * questions_per_minute)
        
        # Question type distribution
        if field in self.question_bank:
            technical_ratio = 0.5 if experience_level in ["senior", "expert"] else 0.4
            behavioral_ratio = 0.3
            scenario_ratio = 0.2
        else:
            field = "general"
            technical_ratio = 0.0
            behavioral_ratio = 0.6
            scenario_ratio = 0.4
        
        # Generate question mix
        session_questions = []
        
        if field != "general" and technical_ratio > 0:
            technical_count = int(total_questions * technical_ratio)
            technical_questions = random.sample(
                self.question_bank[field]["technical"], 
                min(technical_count, len(self.question_bank[field]["technical"]))
            )
            session_questions.extend([
                {"type": "technical", "question": q, "field": field} 
                for q in technical_questions
            ])
        
        # Behavioral questions
        behavioral_count = int(total_questions * behavioral_ratio)
        field_behavioral = self.question_bank.get(field, {}).get("behavioral", [])
        general_behavioral = self.question_bank["general"]["behavioral"]
        all_behavioral = field_behavioral + general_behavioral
        
        behavioral_questions = random.sample(
            all_behavioral, 
            min(behavioral_count, len(all_behavioral))
        )
        session_questions.extend([
            {"type": "behavioral", "question": q, "field": field} 
            for q in behavioral_questions
        ])
        
        # Scenario questions
        remaining_count = total_questions - len(session_questions)
        if remaining_count > 0:
            field_scenarios = self.question_bank.get(field, {}).get("scenario", [])
            general_scenarios = self.question_bank["general"]["scenario"]
            all_scenarios = field_scenarios + general_scenarios
            
            scenario_questions = random.sample(
                all_scenarios, 
                min(remaining_count, len(all_scenarios))
            )
            session_questions.extend([
                {"type": "scenario", "question": q, "field": field} 
                for q in scenario_questions
            ])
        
        # Shuffle questions for variety
        random.shuffle(session_questions)
        
        return {
            "session_id": self._generate_session_id(),
            "field": field,
            "experience_level": experience_level,
            "duration_minutes": duration_minutes,
            "questions": session_questions,
            "evaluation_criteria": self.evaluation_criteria,
            "created_at": datetime.now().isoformat()
        }
    
    def evaluate_response(self, question: Dict, response_text: str, 
                         response_metadata: Dict = None) -> Dict:
        """Evaluate a response using AI-powered analysis"""
        if not response_metadata:
            response_metadata = {}
        
        evaluation = {
            "question": question,
            "response": response_text,
            "scores": {},
            "feedback": {},
            "overall_score": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Analyze response for each criterion
        for criterion, config in self.evaluation_criteria.items():
            score = self._evaluate_criterion(
                criterion, question, response_text, response_metadata
            )
            evaluation["scores"][criterion] = score
            evaluation["feedback"][criterion] = self._generate_criterion_feedback(
                criterion, score, question, response_text
            )
        
        # Calculate weighted overall score
        evaluation["overall_score"] = sum(
            evaluation["scores"][criterion] * config["weight"]
            for criterion, config in self.evaluation_criteria.items()
        )
        
        return evaluation
    
    def _evaluate_criterion(self, criterion: str, question: Dict, 
                          response_text: str, metadata: Dict) -> float:
        """Evaluate a specific criterion (0.0 to 1.0)"""
        response_lower = response_text.lower()
        
        if criterion == "technical_accuracy":
            return self._evaluate_technical_accuracy(question, response_text)
        
        elif criterion == "communication":
            return self._evaluate_communication(response_text)
        
        elif criterion == "problem_solving":
            return self._evaluate_problem_solving(response_text)
        
        elif criterion == "confidence":
            return self._evaluate_confidence(response_text, metadata)
        
        elif criterion == "examples":
            return self._evaluate_examples(response_text)
        
        return 0.5  # Default score
    
    def _evaluate_technical_accuracy(self, question: Dict, response_text: str) -> float:
        """Evaluate technical accuracy of response"""
        response_lower = response_text.lower()
        
        # Define key technical terms for different question types
        technical_keywords = {
            "data_science": [
                "algorithm", "model", "training", "validation", "feature", "dataset",
                "accuracy", "precision", "recall", "overfitting", "underfitting",
                "cross-validation", "bias", "variance", "regression", "classification"
            ],
            "web_development": [
                "html", "css", "javascript", "dom", "api", "http", "server", "client",
                "database", "framework", "library", "asynchronous", "synchronous",
                "responsive", "browser", "debugging", "optimization"
            ]
        }
        
        field = question.get("field", "general")
        relevant_keywords = technical_keywords.get(field, [])
        
        if not relevant_keywords:
            # For non-technical questions, check for structured thinking
            structure_indicators = [
                "first", "second", "then", "because", "therefore", "however",
                "example", "specifically", "in particular"
            ]
            structure_score = sum(1 for word in structure_indicators if word in response_lower)
            return min(structure_score / 3, 1.0)
        
        # Count technical terms used appropriately
        technical_score = sum(1 for term in relevant_keywords if term in response_lower)
        max_possible = min(len(relevant_keywords), 5)  # Cap at 5 for reasonable scoring
        
        return min(technical_score / max_possible, 1.0)
    
    def _evaluate_communication(self, response_text: str) -> float:
        """Evaluate communication clarity"""
        # Basic metrics for communication quality
        sentences = re.split(r'[.!?]+', response_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # Average sentence length (optimal around 15-20 words)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        length_score = max(0, 1 - abs(avg_sentence_length - 17.5) / 17.5)
        
        # Check for transition words
        transition_words = ["however", "therefore", "additionally", "furthermore", 
                          "meanwhile", "consequently", "for example", "in contrast"]
        transition_score = min(
            sum(1 for word in transition_words if word in response_text.lower()) / 2, 1.0
        )
        
        # Check for completeness (has conclusion)
        conclusion_words = ["conclusion", "summary", "overall", "in summary", "to conclude"]
        conclusion_score = 1.0 if any(word in response_text.lower() for word in conclusion_words) else 0.5
        
        return (length_score + transition_score + conclusion_score) / 3
    
    def _evaluate_problem_solving(self, response_text: str) -> float:
        """Evaluate problem-solving approach"""
        response_lower = response_text.lower()
        
        # Look for problem-solving indicators
        approach_indicators = [
            "analyze", "identify", "consider", "evaluate", "compare", "assess",
            "determine", "investigate", "explore", "examine"
        ]
        
        step_indicators = [
            "first", "second", "next", "then", "finally", "step", "approach",
            "process", "method", "strategy"
        ]
        
        approach_score = min(
            sum(1 for word in approach_indicators if word in response_lower) / 3, 1.0
        )
        step_score = min(
            sum(1 for word in step_indicators if word in response_lower) / 2, 1.0
        )
        
        # Check for consideration of alternatives
        alternative_words = ["alternative", "option", "choice", "consider", "could", "might"]
        alternative_score = min(
            sum(1 for word in alternative_words if word in response_lower) / 2, 1.0
        )
        
        return (approach_score + step_score + alternative_score) / 3
    
    def _evaluate_confidence(self, response_text: str, metadata: Dict) -> float:
        """Evaluate confidence in response"""
        response_lower = response_text.lower()
        
        # Confidence indicators (positive)
        confident_words = ["definitely", "certainly", "confident", "sure", "clearly", "obviously"]
        confident_score = min(
            sum(1 for word in confident_words if word in response_lower) / 2, 1.0
        )
        
        # Uncertainty indicators (negative)
        uncertain_words = ["maybe", "perhaps", "possibly", "not sure", "don't know", "uncertain"]
        uncertain_count = sum(1 for word in uncertain_words if word in response_lower)
        uncertainty_penalty = min(uncertain_count / 3, 0.5)
        
        # Response length as confidence indicator
        word_count = len(response_text.split())
        length_confidence = min(word_count / 50, 1.0)  # Normalize around 50 words
        
        # Use speech metadata if available
        speech_confidence = metadata.get("speech_confidence", 0.8)  # Default if not available
        
        final_score = (confident_score + length_confidence + speech_confidence) / 3 - uncertainty_penalty
        return max(0.0, min(1.0, final_score))
    
    def _evaluate_examples(self, response_text: str) -> float:
        """Evaluate use of examples and experiences"""
        response_lower = response_text.lower()
        
        # Example indicators
        example_words = ["example", "instance", "case", "experience", "project", 
                        "situation", "time when", "worked on", "built", "developed"]
        
        example_score = min(
            sum(1 for word in example_words if word in response_lower) / 3, 1.0
        )
        
        # Check for specific details (numbers, names, technologies)
        specific_indicators = [
            r'\d+', # Numbers
            r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', # Proper nouns
            r'\b\w+\.js|\w+\.py|\w+\.java\b' # Technology mentions
        ]
        
        detail_count = sum(len(re.findall(pattern, response_text)) for pattern in specific_indicators)
        detail_score = min(detail_count / 5, 1.0)
        
        return (example_score + detail_score) / 2
    
    def _generate_criterion_feedback(self, criterion: str, score: float, 
                                   question: Dict, response_text: str) -> str:
        """Generate specific feedback for each criterion"""
        if score >= 0.8:
            performance = "excellent"
        elif score >= 0.6:
            performance = "good"
        elif score >= 0.4:
            performance = "fair"
        else:
            performance = "needs improvement"
        
        feedback_templates = {
            "technical_accuracy": {
                "excellent": "Demonstrated strong technical knowledge with accurate information and proper terminology.",
                "good": "Showed good technical understanding with mostly accurate information.",
                "fair": "Basic technical knowledge evident, but could be more detailed or precise.",
                "needs improvement": "Technical accuracy needs improvement. Consider reviewing core concepts."
            },
            "communication": {
                "excellent": "Communicated ideas clearly and effectively with good structure.",
                "good": "Good communication with clear explanations.",
                "fair": "Communication was understandable but could be more structured.",
                "needs improvement": "Work on organizing thoughts and expressing ideas more clearly."
            },
            "problem_solving": {
                "excellent": "Demonstrated excellent problem-solving approach with systematic thinking.",
                "good": "Showed good problem-solving skills with logical reasoning.",
                "fair": "Basic problem-solving approach, could benefit from more structured thinking.",
                "needs improvement": "Focus on developing a more systematic approach to problem-solving."
            },
            "confidence": {
                "excellent": "Displayed strong confidence and composure throughout the response.",
                "good": "Showed good confidence with minor hesitation.",
                "fair": "Some confidence shown but room for improvement in delivery.",
                "needs improvement": "Work on building confidence and reducing uncertainty in responses."
            },
            "examples": {
                "excellent": "Excellent use of specific examples and relevant experiences.",
                "good": "Good use of examples to illustrate points.",
                "fair": "Some examples provided but could be more specific or relevant.",
                "needs improvement": "Include more specific examples and experiences to support your answers."
            }
        }
        
        return feedback_templates.get(criterion, {}).get(performance, 
                                                        "Performance assessment completed.")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = str(random.randint(1000, 9999))
        return f"interview_{timestamp}_{random_suffix}"
    
    def generate_session_summary(self, evaluations: List[Dict]) -> Dict:
        """Generate comprehensive session summary"""
        if not evaluations:
            return {"error": "No evaluations provided"}
        
        # Calculate overall metrics
        overall_scores = [eval_data["overall_score"] for eval_data in evaluations]
        criterion_scores = {}
        
        for criterion in self.evaluation_criteria:
            scores = [eval_data["scores"].get(criterion, 0) for eval_data in evaluations]
            criterion_scores[criterion] = {
                "average": sum(scores) / len(scores),
                "scores": scores
            }
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        
        for criterion, data in criterion_scores.items():
            if data["average"] >= 0.7:
                strengths.append(criterion)
            elif data["average"] <= 0.4:
                weaknesses.append(criterion)
        
        # Generate recommendations
        recommendations = self._generate_session_recommendations(criterion_scores, evaluations)
        
        return {
            "overall_average": sum(overall_scores) / len(overall_scores),
            "question_count": len(evaluations),
            "criterion_averages": {k: v["average"] for k, v in criterion_scores.items()},
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "detailed_scores": criterion_scores
        }
    
    def _generate_session_recommendations(self, criterion_scores: Dict, 
                                        evaluations: List[Dict]) -> List[str]:
        """Generate personalized recommendations based on performance"""
        recommendations = []
        
        # Criterion-specific recommendations
        for criterion, data in criterion_scores.items():
            if data["average"] <= 0.5:
                if criterion == "technical_accuracy":
                    recommendations.append(
                        "Review fundamental concepts and practice explaining technical topics clearly."
                    )
                elif criterion == "communication":
                    recommendations.append(
                        "Practice structuring your responses with clear introductions and conclusions."
                    )
                elif criterion == "problem_solving":
                    recommendations.append(
                        "Work on developing a systematic approach to problem-solving."
                    )
                elif criterion == "confidence":
                    recommendations.append(
                        "Practice interviewing to build confidence and reduce hesitation."
                    )
                elif criterion == "examples":
                    recommendations.append(
                        "Prepare specific examples from your experience to illustrate your points."
                    )
        
        # Overall recommendations
        overall_avg = sum(data["average"] for data in criterion_scores.values()) / len(criterion_scores)
        
        if overall_avg < 0.6:
            recommendations.append("Consider doing additional mock interviews to improve overall performance.")
        
        if not recommendations:
            recommendations.append("Great job! Continue practicing to maintain your strong performance.")
        
        return recommendations