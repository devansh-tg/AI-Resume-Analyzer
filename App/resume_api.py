"""
Resume Analytics API for Bulk Processing
Provides REST API endpoints for recruiters and organizations
"""

from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
import tempfile
import zipfile
from io import BytesIO, StringIO
import traceback

# Import our custom modules
from enhanced_analyzer import EnhancedResumeAnalyzer, JobMatcher, CareerPredictor
from mock_interview import MockInterviewEngine
from pyresparser import ResumeParser
import pandas as pd

class ResumeAnalyticsAPI:
    """Flask API for resume analytics and bulk processing"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
        self.app.config['UPLOAD_FOLDER'] = '/tmp/resume_uploads'
        
        # Initialize analyzers
        self.enhanced_analyzer = EnhancedResumeAnalyzer()
        self.job_matcher = JobMatcher()
        self.career_predictor = CareerPredictor()
        self.interview_engine = MockInterviewEngine()
        
        # Ensure upload directory exists
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Setup routes
        self._setup_routes()
        
        # API key for authentication (in production, use proper auth)
        self.valid_api_keys = {
            "demo_key_123": {"name": "Demo Organization", "tier": "basic"},
            "premium_key_456": {"name": "Premium Corp", "tier": "premium"}
        }
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0"
            })
        
        @self.app.route('/api/analyze/single', methods=['POST'])
        def analyze_single_resume():
            """Analyze a single resume"""
            try:
                # Check API key
                auth_result = self._authenticate_request(request)
                if not auth_result["valid"]:
                    return jsonify({"error": "Invalid API key"}), 401
                
                # Check file upload
                if 'resume' not in request.files:
                    return jsonify({"error": "No resume file provided"}), 400
                
                file = request.files['resume']
                if file.filename == '':
                    return jsonify({"error": "No file selected"}), 400
                
                # Process resume
                result = self._process_single_resume(file, request.form)
                return jsonify(result)
                
            except Exception as e:
                return jsonify({
                    "error": "Internal server error",
                    "details": str(e) if self.app.debug else "Contact support"
                }), 500
        
        @self.app.route('/api/analyze/bulk', methods=['POST'])
        def analyze_bulk_resumes():
            """Analyze multiple resumes in bulk"""
            try:
                # Check API key and tier
                auth_result = self._authenticate_request(request)
                if not auth_result["valid"]:
                    return jsonify({"error": "Invalid API key"}), 401
                
                if auth_result["tier"] != "premium":
                    return jsonify({"error": "Bulk analysis requires premium tier"}), 403
                
                # Process bulk upload
                if 'resumes' not in request.files:
                    return jsonify({"error": "No resume files provided"}), 400
                
                files = request.files.getlist('resumes')
                results = self._process_bulk_resumes(files, request.form)
                
                return jsonify(results)
                
            except Exception as e:
                return jsonify({
                    "error": "Internal server error",
                    "details": str(e) if self.app.debug else "Contact support"
                }), 500
        
        @self.app.route('/api/match/job', methods=['POST'])
        def match_job_description():
            """Match resume against job description"""
            try:
                auth_result = self._authenticate_request(request)
                if not auth_result["valid"]:
                    return jsonify({"error": "Invalid API key"}), 401
                
                data = request.get_json()
                if not data or 'resume_text' not in data or 'job_description' not in data:
                    return jsonify({"error": "Missing resume_text or job_description"}), 400
                
                match_result = self.job_matcher.match_resume_to_job(
                    data['resume_text'],
                    data['job_description']
                )
                
                return jsonify({
                    "match_analysis": match_result,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({
                    "error": "Internal server error",
                    "details": str(e) if self.app.debug else "Contact support"
                }), 500
        
        @self.app.route('/api/interview/generate', methods=['POST'])
        def generate_interview():
            """Generate mock interview session"""
            try:
                auth_result = self._authenticate_request(request)
                if not auth_result["valid"]:
                    return jsonify({"error": "Invalid API key"}), 401
                
                data = request.get_json()
                field = data.get('field', 'general')
                experience_level = data.get('experience_level', 'mid')
                duration = data.get('duration_minutes', 30)
                
                interview_session = self.interview_engine.generate_interview_session(
                    field, experience_level, duration
                )
                
                return jsonify(interview_session)
                
            except Exception as e:
                return jsonify({
                    "error": "Internal server error",
                    "details": str(e) if self.app.debug else "Contact support"
                }), 500
        
        @self.app.route('/api/export/csv', methods=['POST'])
        def export_analysis_csv():
            """Export analysis results as CSV"""
            try:
                auth_result = self._authenticate_request(request)
                if not auth_result["valid"]:
                    return jsonify({"error": "Invalid API key"}), 401
                
                data = request.get_json()
                analysis_results = data.get('analysis_results', [])
                
                if not analysis_results:
                    return jsonify({"error": "No analysis results provided"}), 400
                
                csv_file = self._create_csv_export(analysis_results)
                
                return send_file(
                    csv_file,
                    as_attachment=True,
                    download_name=f'resume_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mimetype='text/csv'
                )
                
            except Exception as e:
                return jsonify({
                    "error": "Internal server error",
                    "details": str(e) if self.app.debug else "Contact support"
                }), 500
        
        @self.app.route('/api/stats/usage', methods=['GET'])
        def get_usage_stats():
            """Get API usage statistics"""
            try:
                auth_result = self._authenticate_request(request)
                if not auth_result["valid"]:
                    return jsonify({"error": "Invalid API key"}), 401
                
                # In a real implementation, this would query a database
                stats = {
                    "api_key": auth_result["name"],
                    "tier": auth_result["tier"],
                    "current_month": {
                        "requests": 150,
                        "resumes_processed": 127,
                        "bulk_analyses": 5
                    },
                    "limits": {
                        "monthly_requests": 1000 if auth_result["tier"] == "premium" else 100,
                        "bulk_analysis": auth_result["tier"] == "premium"
                    }
                }
                
                return jsonify(stats)
                
            except Exception as e:
                return jsonify({
                    "error": "Internal server error",
                    "details": str(e) if self.app.debug else "Contact support"
                }), 500
    
    def _authenticate_request(self, request) -> Dict:
        """Authenticate API request"""
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key or api_key not in self.valid_api_keys:
            return {"valid": False}
        
        user_info = self.valid_api_keys[api_key]
        return {
            "valid": True,
            "name": user_info["name"],
            "tier": user_info["tier"]
        }
    
    def _process_single_resume(self, file, form_data: Dict) -> Dict:
        """Process a single resume file"""
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Parse resume using pyresparser
            parser = ResumeParser(file_path)
            basic_data = parser.get_extracted_data()
            
            # Read file content for text analysis
            from advanced_nlp import AdvancedNLPEngine
            nlp_engine = AdvancedNLPEngine()
            
            # Extract text based on file type
            resume_text = self._extract_text_from_file(file_path)
            
            # Enhanced analysis
            analysis_result = self.enhanced_analyzer.comprehensive_analysis(resume_text, basic_data)
            
            # Add career prediction if requested
            include_career_prediction = form_data.get('include_career_prediction', 'false').lower() == 'true'
            if include_career_prediction:
                career_prediction = self.career_predictor.predict_career_trajectory(analysis_result)
                analysis_result['career_prediction'] = career_prediction
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return {
                "status": "success",
                "filename": filename,
                "analysis": analysis_result,
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            # Clean up on error
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            raise e
    
    def _process_bulk_resumes(self, files: List, form_data: Dict) -> Dict:
        """Process multiple resume files"""
        results = []
        errors = []
        
        for file in files:
            try:
                if file.filename == '':
                    continue
                    
                # Process individual file
                result = self._process_single_resume(file, form_data)
                results.append(result)
                
            except Exception as e:
                errors.append({
                    "filename": file.filename,
                    "error": str(e)
                })
        
        # Generate summary statistics
        if results:
            scores = [r["analysis"]["overall_score"]["overall"] for r in results]
            summary = {
                "total_processed": len(results),
                "average_score": sum(scores) / len(scores),
                "score_distribution": {
                    "excellent": len([s for s in scores if s >= 0.8]),
                    "good": len([s for s in scores if 0.6 <= s < 0.8]),
                    "fair": len([s for s in scores if 0.4 <= s < 0.6]),
                    "poor": len([s for s in scores if s < 0.4])
                }
            }
        else:
            summary = {"total_processed": 0}
        
        return {
            "status": "completed",
            "summary": summary,
            "results": results,
            "errors": errors,
            "processed_at": datetime.now().isoformat()
        }
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from uploaded file"""
        try:
            if file_path.endswith('.pdf'):
                # Use existing PDF extraction logic
                from App import pdf_reader
                return pdf_reader(open(file_path, 'rb'))
            elif file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                # For other formats, try to read as text
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def _create_csv_export(self, analysis_results: List[Dict]) -> BytesIO:
        """Create CSV export of analysis results"""
        output = StringIO()
        
        # Define CSV columns
        columns = [
            'filename', 'name', 'email', 'mobile_number', 'overall_score',
            'content_quality', 'skill_relevance', 'experience_depth',
            'primary_field', 'experience_level', 'predicted_salary', 'skills_count'
        ]
        
        writer = csv.DictWriter(output, fieldnames=columns)
        writer.writeheader()
        
        for result in analysis_results:
            analysis = result.get('analysis', {})
            basic_info = analysis.get('basic_info', {})
            scores = analysis.get('overall_score', {})
            ai_insights = analysis.get('ai_insights', {})
            benchmarking = analysis.get('benchmarking', {})
            
            row = {
                'filename': result.get('filename', ''),
                'name': basic_info.get('name', ''),
                'email': basic_info.get('email', ''),
                'mobile_number': basic_info.get('mobile_number', ''),
                'overall_score': scores.get('overall', 0),
                'content_quality': scores.get('content_quality', 0),
                'skill_relevance': scores.get('skill_relevance', 0),
                'experience_depth': scores.get('experience_depth', 0),
                'primary_field': ai_insights.get('primary_field', ''),
                'experience_level': self._get_max_experience_level(analysis),
                'predicted_salary': benchmarking.get('salary_projection', {}).get('projected_salary', ''),
                'skills_count': len(basic_info.get('skills', []))
            }
            writer.writerow(row)
        
        # Convert to BytesIO
        output.seek(0)
        bytes_output = BytesIO()
        bytes_output.write(output.getvalue().encode('utf-8'))
        bytes_output.seek(0)
        
        return bytes_output
    
    def _get_max_experience_level(self, analysis: Dict) -> str:
        """Get the most likely experience level"""
        experience_levels = analysis.get('advanced_metrics', {}).get('experience_level', {})
        if experience_levels:
            return max(experience_levels, key=experience_levels.get)
        return 'unknown'
    
    def run(self, host='localhost', port=5000, debug=False):
        """Run the Flask API server"""
        self.app.run(host=host, port=port, debug=debug)

# API Documentation Generator
class APIDocGenerator:
    """Generate API documentation"""
    
    @staticmethod
    def generate_openapi_spec() -> Dict:
        """Generate OpenAPI specification for the API"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": "Resume Analytics API",
                "version": "2.0.0",
                "description": "Advanced AI-powered resume analysis and processing API"
            },
            "servers": [
                {"url": "http://localhost:5000", "description": "Development server"}
            ],
            "security": [
                {"ApiKeyAuth": []}
            ],
            "components": {
                "securitySchemes": {
                    "ApiKeyAuth": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "X-API-Key"
                    }
                }
            },
            "paths": {
                "/api/health": {
                    "get": {
                        "summary": "Health check",
                        "responses": {
                            "200": {
                                "description": "Service is healthy",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "status": {"type": "string"},
                                                "timestamp": {"type": "string"},
                                                "version": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/analyze/single": {
                    "post": {
                        "summary": "Analyze single resume",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "resume": {
                                                "type": "string",
                                                "format": "binary"
                                            },
                                            "include_career_prediction": {
                                                "type": "boolean"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Analysis completed successfully"
                            },
                            "400": {
                                "description": "Bad request"
                            },
                            "401": {
                                "description": "Unauthorized"
                            }
                        }
                    }
                },
                "/api/analyze/bulk": {
                    "post": {
                        "summary": "Analyze multiple resumes (Premium tier only)",
                        "requestBody": {
                            "content": {
                                "multipart/form-data": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "resumes": {
                                                "type": "array",
                                                "items": {
                                                    "type": "string",
                                                    "format": "binary"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Bulk analysis completed"
                            },
                            "403": {
                                "description": "Premium tier required"
                            }
                        }
                    }
                },
                "/api/match/job": {
                    "post": {
                        "summary": "Match resume to job description",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "resume_text": {"type": "string"},
                                            "job_description": {"type": "string"}
                                        },
                                        "required": ["resume_text", "job_description"]
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Job matching analysis completed"
                            }
                        }
                    }
                }
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Create API instance
    api = ResumeAnalyticsAPI()
    
    # Generate API documentation
    doc_generator = APIDocGenerator()
    openapi_spec = doc_generator.generate_openapi_spec()
    
    # Save API documentation
    with open('/tmp/api_documentation.json', 'w') as f:
        json.dump(openapi_spec, f, indent=2)
    
    print("API Documentation generated: /tmp/api_documentation.json")
    print("Starting Resume Analytics API server...")
    print("Available endpoints:")
    print("- GET  /api/health")
    print("- POST /api/analyze/single")
    print("- POST /api/analyze/bulk")
    print("- POST /api/match/job")
    print("- POST /api/interview/generate")
    print("- POST /api/export/csv")
    print("- GET  /api/stats/usage")
    
    # Run the API server
    api.run(debug=True)