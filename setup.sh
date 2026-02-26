#!/bin/bash

# GruhaAlankar - Local Development Setup Script

set -e

echo "🚀 GruhaAlankar Setup Script"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python 3 found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found"

# Backend Setup
echo ""
echo "📦 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Setup environment
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  .env file created. Please configure your credentials!"
fi

cd ..

# Frontend Setup
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Install dependencies
npm install
echo "✅ Frontend dependencies installed"

# Setup environment
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Frontend .env created"
fi

cd ..

echo ""
echo "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "📝 Next Steps:"
echo "1. Add Firebase credentials to backend/firebase-credentials.json"
echo "2. Configure backend/.env with your API keys"
echo "3. Run backend: cd backend && python app.py"
echo "4. Run frontend: cd frontend && npm run dev"
echo ""
echo "📚 Documentation: README.md"
echo "🚀 Happy coding!"
