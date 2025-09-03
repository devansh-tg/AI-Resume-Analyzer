#!/bin/bash

# Enhanced AI Resume Analyzer Installation Script
echo "🚀 Setting up Enhanced AI Resume Analyzer..."

# Check Python version
python_version=$(python3 --version 2>/dev/null || python --version 2>/dev/null || echo "Python not found")
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv 2>/dev/null || python -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate 2>/dev/null || venv\Scripts\activate.bat

# Install essential dependencies first
echo "📚 Installing essential dependencies..."
pip install --upgrade pip

# Core dependencies
pip install streamlit pandas numpy

# Enhanced features (optional, with fallbacks)
echo "🤖 Installing AI/ML dependencies..."
pip install --quiet scikit-learn || echo "⚠️  scikit-learn installation failed - some AI features may be limited"
pip install --quiet plotly || echo "⚠️  plotly installation failed - using basic visualizations"
pip install --quiet flask || echo "⚠️  flask installation failed - API features disabled"

# Try to install transformers (may fail due to dependencies)
pip install --quiet transformers || echo "⚠️  transformers installation failed - using fallback NLP"
pip install --quiet sentence-transformers || echo "⚠️  sentence-transformers installation failed - using basic similarity"

# Original dependencies
echo "📋 Installing original resume parser dependencies..."
pip install --quiet pymysql || echo "⚠️  pymysql installation failed - using SQLite fallback"
pip install --quiet streamlit-tags || echo "⚠️  streamlit-tags installation failed - using basic input"
pip install --quiet pdfminer3 || echo "⚠️  pdfminer3 installation failed - PDF processing may be limited"
pip install --quiet pyresparser || echo "⚠️  pyresparser installation failed - using basic text extraction"

# NLP dependencies
echo "🔤 Installing NLP dependencies..."
pip install --quiet nltk || echo "⚠️  nltk installation failed"
pip install --quiet spacy || echo "⚠️  spacy installation failed"

# Try to download spacy model
python -m spacy download en_core_web_sm 2>/dev/null || echo "⚠️  spaCy model download failed - using basic processing"

# Download NLTK data
python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('punkt', quiet=True)" 2>/dev/null || echo "⚠️  NLTK data download failed"

echo "✅ Installation complete!"
echo ""
echo "🎯 To run the Enhanced AI Resume Analyzer:"
echo "   cd App"
echo "   streamlit run enhanced_app.py"
echo ""
echo "📊 To run the original version:"
echo "   cd App" 
echo "   streamlit run App.py"
echo ""
echo "🧪 To test the system:"
echo "   cd App"
echo "   python test_enhanced_system.py"
echo ""
echo "💡 Note: Some advanced AI features may be limited based on available dependencies."