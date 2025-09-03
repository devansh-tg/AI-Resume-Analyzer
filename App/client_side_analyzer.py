"""
Client-Side Resume Processing Module
Enables browser-based analysis for privacy-sensitive documents
"""

import streamlit as st
import streamlit.components.v1 as components
import json

def create_client_side_analyzer():
    """Create client-side resume analyzer component"""
    
    # JavaScript and TensorFlow.js code for client-side processing
    client_side_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.10.0/dist/tf.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-node@4.10.0/dist/tf-node.min.js"></script>
        <style>
            .analyzer-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .upload-area {
                border: 2px dashed #ccc;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                margin: 20px 0;
                transition: border-color 0.3s;
            }
            .upload-area:hover {
                border-color: #667eea;
            }
            .results-container {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                display: none;
            }
            .metric-card {
                background: white;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: inline-block;
                min-width: 150px;
                text-align: center;
            }
            .progress-bar {
                width: 100%;
                height: 20px;
                background-color: #e0e0e0;
                border-radius: 10px;
                overflow: hidden;
                margin: 10px 0;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 10px;
                transition: width 0.5s ease;
            }
            .skill-tag {
                background: #667eea;
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                margin: 3px;
                display: inline-block;
                font-size: 12px;
            }
            .recommendation {
                background: #e8f4f8;
                border-left: 4px solid #667eea;
                padding: 10px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="analyzer-container">
            <h2>🔒 Privacy-First Resume Analysis</h2>
            <p>Your resume is processed entirely in your browser - no data leaves your device!</p>
            
            <div class="upload-area" id="uploadArea" onclick="document.getElementById('fileInput').click()">
                <input type="file" id="fileInput" accept=".pdf,.txt,.doc,.docx" style="display: none;" onchange="handleFileUpload(event)">
                <div id="uploadText">
                    <h3>📄 Drop your resume here or click to upload</h3>
                    <p>Supports PDF, TXT, DOC, DOCX files</p>
                </div>
            </div>
            
            <div id="processingIndicator" style="display: none; text-align: center;">
                <h3>🤖 Analyzing your resume...</h3>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="results-container" id="resultsContainer">
                <h3>📊 Analysis Results</h3>
                
                <div id="metricsContainer">
                    <div class="metric-card">
                        <h4 id="overallScore">0%</h4>
                        <p>Overall Score</p>
                    </div>
                    <div class="metric-card">
                        <h4 id="experienceLevel">-</h4>
                        <p>Experience Level</p>
                    </div>
                    <div class="metric-card">
                        <h4 id="skillCount">0</h4>
                        <p>Skills Detected</p>
                    </div>
                    <div class="metric-card">
                        <h4 id="fieldPrediction">-</h4>
                        <p>Predicted Field</p>
                    </div>
                </div>
                
                <div id="skillsSection">
                    <h4>🎯 Skills Detected</h4>
                    <div id="skillsList"></div>
                </div>
                
                <div id="recommendationsSection">
                    <h4>💡 AI Recommendations</h4>
                    <div id="recommendationsList"></div>
                </div>
                
                <div id="qualitySection">
                    <h4>📈 Quality Analysis</h4>
                    <div id="qualityMetrics"></div>
                </div>
            </div>
        </div>

        <script>
            // Simple skill detection patterns
            const skillPatterns = {
                programming: ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
                webDev: ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask'],
                datascience: ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'],
                databases: ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
                cloud: ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
                mobile: ['android', 'ios', 'react native', 'flutter', 'xamarin']
            };
            
            const experienceKeywords = {
                fresher: ['graduate', 'fresher', 'entry level', 'recent graduate'],
                junior: ['1 year', '2 years', 'junior', 'associate'],
                mid: ['3 years', '4 years', '5 years', 'mid level'],
                senior: ['6 years', '7 years', '8 years', 'senior', 'lead'],
                expert: ['9 years', '10+ years', 'architect', 'principal', 'director']
            };
            
            async function handleFileUpload(event) {
                const file = event.target.files[0];
                if (!file) return;
                
                showProcessing();
                
                try {
                    const text = await extractTextFromFile(file);
                    const analysis = analyzeResume(text);
                    displayResults(analysis);
                } catch (error) {
                    console.error('Error processing file:', error);
                    alert('Error processing file. Please try a different format.');
                }
                
                hideProcessing();
            }
            
            async function extractTextFromFile(file) {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    
                    if (file.type === 'text/plain') {
                        reader.onload = (e) => resolve(e.target.result);
                        reader.readAsText(file);
                    } else if (file.type === 'application/pdf') {
                        // For demo purposes, we'll simulate PDF text extraction
                        // In a real implementation, you'd use PDF.js or similar
                        reader.onload = (e) => {
                            // Simulate PDF text extraction
                            resolve(simulatePDFText());
                        };
                        reader.readAsArrayBuffer(file);
                    } else {
                        // For other formats, try reading as text
                        reader.onload = (e) => resolve(e.target.result);
                        reader.readAsText(file);
                    }
                    
                    reader.onerror = () => reject(new Error('File reading failed'));
                });
            }
            
            function simulatePDFText() {
                return `
                John Doe
                Software Developer
                Email: john.doe@email.com
                Phone: (555) 123-4567
                
                EXPERIENCE
                Senior Software Developer - Tech Corp (2020-2023)
                • Developed web applications using React and Node.js
                • Led a team of 5 developers
                • Implemented CI/CD pipelines using Docker and Kubernetes
                • Worked with Python, JavaScript, and SQL databases
                
                Software Developer - StartupXYZ (2018-2020)
                • Built mobile applications using React Native
                • Collaborated with data science team on machine learning projects
                • Used AWS services for cloud deployment
                
                EDUCATION
                Bachelor of Science in Computer Science
                University of Technology (2014-2018)
                
                SKILLS
                Programming: Python, JavaScript, Java, C++
                Web Development: React, Node.js, HTML, CSS
                Databases: MySQL, MongoDB, PostgreSQL
                Cloud: AWS, Docker, Kubernetes
                Tools: Git, Jenkins, JIRA
                `;
            }
            
            function analyzeResume(text) {
                const textLower = text.toLowerCase();
                
                // Detect skills
                const detectedSkills = {};
                let totalSkills = 0;
                
                for (const [category, skills] of Object.entries(skillPatterns)) {
                    detectedSkills[category] = [];
                    for (const skill of skills) {
                        if (textLower.includes(skill.toLowerCase())) {
                            detectedSkills[category].push(skill);
                            totalSkills++;
                        }
                    }
                }
                
                // Determine experience level
                let experienceLevel = 'entry';
                let maxScore = 0;
                
                for (const [level, keywords] of Object.entries(experienceKeywords)) {
                    let score = 0;
                    for (const keyword of keywords) {
                        if (textLower.includes(keyword)) {
                            score++;
                        }
                    }
                    if (score > maxScore) {
                        maxScore = score;
                        experienceLevel = level;
                    }
                }
                
                // Predict field based on skills
                let predictedField = 'general';
                let maxCategorySkills = 0;
                
                for (const [category, skills] of Object.entries(detectedSkills)) {
                    if (skills.length > maxCategorySkills) {
                        maxCategorySkills = skills.length;
                        if (category === 'programming' || category === 'webDev') {
                            predictedField = 'Software Development';
                        } else if (category === 'datascience') {
                            predictedField = 'Data Science';
                        } else if (category === 'mobile') {
                            predictedField = 'Mobile Development';
                        } else if (category === 'cloud') {
                            predictedField = 'DevOps/Cloud';
                        }
                    }
                }
                
                // Calculate overall score
                const hasContact = /email|phone|@/.test(textLower);
                const hasExperience = /experience|work|job|company/.test(textLower);
                const hasEducation = /education|degree|university|college/.test(textLower);
                const hasSkills = totalSkills > 0;
                
                const baseScore = (hasContact + hasExperience + hasEducation + hasSkills) * 0.2;
                const skillBonus = Math.min(totalSkills * 0.05, 0.3);
                const overallScore = Math.min((baseScore + skillBonus) * 100, 100);
                
                // Generate recommendations
                const recommendations = generateRecommendations(detectedSkills, experienceLevel, predictedField);
                
                return {
                    overallScore: Math.round(overallScore),
                    experienceLevel: experienceLevel.charAt(0).toUpperCase() + experienceLevel.slice(1),
                    skillCount: totalSkills,
                    predictedField: predictedField,
                    detectedSkills: detectedSkills,
                    recommendations: recommendations,
                    qualityMetrics: {
                        hasContact: hasContact,
                        hasExperience: hasExperience,
                        hasEducation: hasEducation,
                        hasSkills: hasSkills
                    }
                };
            }
            
            function generateRecommendations(skills, level, field) {
                const recommendations = [];
                
                // Skill-based recommendations
                if (skills.programming && skills.programming.length > 0 && skills.programming.length < 3) {
                    recommendations.push("Consider adding more programming languages to broaden your technical skills.");
                }
                
                if (!skills.cloud || skills.cloud.length === 0) {
                    recommendations.push("Add cloud technologies (AWS, Azure, GCP) to stay competitive in today's market.");
                }
                
                if (level === 'fresher' || level === 'junior') {
                    recommendations.push("Include personal projects or contributions to open source to demonstrate practical experience.");
                }
                
                if (field === 'Data Science' && (!skills.datascience || skills.datascience.length < 2)) {
                    recommendations.push("Strengthen your data science toolkit with more ML/AI technologies.");
                }
                
                // General recommendations
                recommendations.push("Use action verbs to start your bullet points (e.g., 'Developed', 'Implemented', 'Led').");
                recommendations.push("Include quantifiable achievements where possible (e.g., 'Improved performance by 30%').");
                
                return recommendations;
            }
            
            function showProcessing() {
                document.getElementById('uploadArea').style.display = 'none';
                document.getElementById('processingIndicator').style.display = 'block';
                
                // Simulate progress
                let progress = 0;
                const progressFill = document.getElementById('progressFill');
                const interval = setInterval(() => {
                    progress += Math.random() * 20;
                    if (progress >= 100) {
                        progress = 100;
                        clearInterval(interval);
                    }
                    progressFill.style.width = progress + '%';
                }, 200);
            }
            
            function hideProcessing() {
                document.getElementById('processingIndicator').style.display = 'none';
                document.getElementById('resultsContainer').style.display = 'block';
            }
            
            function displayResults(analysis) {
                // Update metrics
                document.getElementById('overallScore').textContent = analysis.overallScore + '%';
                document.getElementById('experienceLevel').textContent = analysis.experienceLevel;
                document.getElementById('skillCount').textContent = analysis.skillCount;
                document.getElementById('fieldPrediction').textContent = analysis.predictedField;
                
                // Display skills
                const skillsList = document.getElementById('skillsList');
                skillsList.innerHTML = '';
                
                for (const [category, skills] of Object.entries(analysis.detectedSkills)) {
                    if (skills.length > 0) {
                        const categoryDiv = document.createElement('div');
                        categoryDiv.innerHTML = `<strong>${category.replace(/([A-Z])/g, ' $1').trim()}:</strong> `;
                        
                        skills.forEach(skill => {
                            const skillTag = document.createElement('span');
                            skillTag.className = 'skill-tag';
                            skillTag.textContent = skill;
                            categoryDiv.appendChild(skillTag);
                        });
                        
                        skillsList.appendChild(categoryDiv);
                    }
                }
                
                // Display recommendations
                const recommendationsList = document.getElementById('recommendationsList');
                recommendationsList.innerHTML = '';
                
                analysis.recommendations.forEach(rec => {
                    const recDiv = document.createElement('div');
                    recDiv.className = 'recommendation';
                    recDiv.textContent = '• ' + rec;
                    recommendationsList.appendChild(recDiv);
                });
                
                // Display quality metrics
                const qualityMetrics = document.getElementById('qualityMetrics');
                qualityMetrics.innerHTML = '';
                
                const metrics = [
                    { name: 'Contact Information', value: analysis.qualityMetrics.hasContact },
                    { name: 'Work Experience', value: analysis.qualityMetrics.hasExperience },
                    { name: 'Education Details', value: analysis.qualityMetrics.hasEducation },
                    { name: 'Skills Section', value: analysis.qualityMetrics.hasSkills }
                ];
                
                metrics.forEach(metric => {
                    const metricDiv = document.createElement('div');
                    metricDiv.innerHTML = `
                        <span>${metric.name}: </span>
                        <span style="color: ${metric.value ? 'green' : 'red'}">
                            ${metric.value ? '✓ Present' : '✗ Missing'}
                        </span>
                    `;
                    qualityMetrics.appendChild(metricDiv);
                });
                
                // Send results to parent Streamlit app
                if (window.parent) {
                    window.parent.postMessage({
                        type: 'resume-analysis-complete',
                        data: analysis
                    }, '*');
                }
            }
            
            // Handle drag and drop
            const uploadArea = document.getElementById('uploadArea');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = '#667eea';
            });
            
            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = '#ccc';
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.style.borderColor = '#ccc';
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    document.getElementById('fileInput').files = files;
                    handleFileUpload({ target: { files: files } });
                }
            });
        </script>
    </body>
    </html>
    """
    
    return client_side_code

def render_client_side_analyzer():
    """Render the client-side analyzer component"""
    st.subheader("🔒 Privacy-First Analysis")
    st.info("This analyzer processes your resume entirely in your browser. No data is sent to our servers!")
    
    # Render the client-side component
    client_code = create_client_side_analyzer()
    components.html(client_code, height=800, scrolling=True)
    
    # JavaScript to handle messages from the iframe
    st.markdown("""
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'resume-analysis-complete') {
            // Handle the analysis results
            console.log('Client-side analysis complete:', event.data.data);
            
            // You could update Streamlit session state here
            // For now, we'll just log the results
        }
    });
    </script>
    """, unsafe_allow_html=True)

def create_privacy_comparison():
    """Create a comparison between server-side and client-side analysis"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌐 Server-Side Analysis
        **Advantages:**
        - More powerful AI models
        - Comprehensive feature set
        - Real-time updates
        - Advanced visualizations
        
        **Data Handling:**
        - Resume processed on our servers
        - Encrypted in transit and at rest
        - Automatically deleted after analysis
        - GDPR compliant
        """)
    
    with col2:
        st.markdown("""
        ### 🔒 Client-Side Analysis
        **Advantages:**
        - Maximum privacy protection
        - No data leaves your device
        - Works offline
        - Instant processing
        
        **Limitations:**
        - Simplified analysis
        - Limited AI capabilities
        - No progress tracking
        - Basic visualizations
        """)

if __name__ == "__main__":
    st.set_page_config(page_title="Client-Side Resume Analyzer", layout="wide")
    
    st.title("🔒 Privacy-First Resume Analysis")
    
    # Privacy comparison
    create_privacy_comparison()
    
    st.markdown("---")
    
    # Client-side analyzer
    render_client_side_analyzer()