#!/bin/bash
# Setup script for Documentation Quality Analyzer
# Creates virtual environment and installs dependencies

set -e

echo "📦 Setting up Documentation Quality Analyzer..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📂 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Copy .env.example to .env and configure:"
echo "     cp .env.example .env"
echo "     # Edit .env and add your ANTHROPIC_API_KEY (optional)"
echo ""
echo "  3. Run the analyzer:"
echo "     python doc_analyzer.py /path/to/docs"
echo ""
echo "  4. Or run tests:"
echo "     pytest test_analyzer.py -v"
echo ""
echo "To deactivate the virtual environment later, run: deactivate"
