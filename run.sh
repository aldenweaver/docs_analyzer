#!/bin/bash
# Convenience script to run the analyzer with venv activated

set -e

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. AI analysis will be disabled."
    echo "   To enable AI analysis, copy .env.example to .env and add your API key."
    echo ""
fi

# Run the analyzer with all provided arguments
python doc_analyzer.py "$@"
