#!/bin/bash
# Automated setup verification script
# Run this after pulling to check if everything is setup correctly

echo "========================================"
echo "Weekly Report Agent - Setup Verification"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_status() {
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} $1"
  else
    echo -e "${RED}✗${NC} $1"
  fi
}

# Check Python
echo "Checking Python..."
python --version > /dev/null 2>&1
check_status "Python installed"

# Check Node
echo "Checking Node.js..."
node --version > /dev/null 2>&1
check_status "Node.js installed"

# Check npm
echo "Checking npm..."
npm --version > /dev/null 2>&1
check_status "npm installed"

# Check Git
echo "Checking Git..."
git --version > /dev/null 2>&1
check_status "Git installed"

echo ""
echo "Checking Backend..."

# Check backend folder
if [ -d "backend" ]; then
  echo -e "${GREEN}✓${NC} Backend folder exists"
  
  # Check requirements.txt
  if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✓${NC} requirements.txt found"
  else
    echo -e "${RED}✗${NC} requirements.txt missing"
  fi
  
  # Check .env
  if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} .env file found"
  else
    echo -e "${YELLOW}⚠${NC} .env file missing (run: cp backend/.env.example backend/.env)"
  fi
else
  echo -e "${RED}✗${NC} Backend folder not found"
fi

echo ""
echo "Checking Frontend..."

# Check frontend folder
if [ -d "frontend" ]; then
  echo -e "${GREEN}✓${NC} Frontend folder exists"
  
  # Check package.json
  if [ -f "frontend/package.json" ]; then
    echo -e "${GREEN}✓${NC} package.json found"
  else
    echo -e "${RED}✗${NC} package.json missing"
  fi
  
  # Check .env.local
  if [ -f "frontend/.env.local" ]; then
    echo -e "${GREEN}✓${NC} .env.local file found"
  else
    echo -e "${YELLOW}⚠${NC} .env.local file missing (run: cp frontend/.env.example frontend/.env.local)"
  fi
else
  echo -e "${RED}✗${NC} Frontend folder not found"
fi

echo ""
echo "========================================"
echo "Setup Verification Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Setup Backend:"
echo "   cd backend"
echo "   python -m venv venv"
echo "   source venv/bin/activate  # or: venv\\Scripts\\activate on Windows"
echo "   pip install -r requirements.txt"
echo "   cp .env.example .env"
echo "   # Edit .env and add GEMINI_API_KEY"
echo "   python -m uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. Setup Frontend (in another terminal):"
echo "   cd frontend"
echo "   npm install"
echo "   cp .env.example .env.local"
echo "   npm run dev"
echo ""
echo "3. Open browser: http://localhost:5173"
