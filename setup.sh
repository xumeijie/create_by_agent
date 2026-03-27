#!/bin/bash
# Setup script for new test automation project
# Usage: chmod +x setup.sh && ./setup.sh

set -e

echo "=========================================="
echo "Test Automation Framework Setup"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "✓ Creating report directories..."
mkdir -p reports/html
mkdir -p reports/allure-results

# Display next steps
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Update configuration:"
echo "   Edit config/environments.yaml with your system details"
echo ""
echo "2. Create your first test:"
echo "   Create tests/test_my_api.py"
echo ""
echo "3. Run tests:"
echo "   pytest tests/"
echo ""
echo "4. View this guide:"
echo "   cat QUICKSTART.md"
echo ""
echo "Happy testing! 🚀"
echo ""
