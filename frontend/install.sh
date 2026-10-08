#!/bin/bash
# Installation script for your teammate
# Run: bash install.sh

set -e

echo "============================================"
echo "Weekly Report Agent Frontend Setup"
echo "============================================"
echo ""

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 16+ from https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node -v)
echo "✅ Node.js detected: $NODE_VERSION"
echo ""

# Check npm version
NPM_VERSION=$(npm -v)
echo "✅ npm detected: $NPM_VERSION"
echo ""

# Navigate to frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found"
    echo "Please run this script from the frontend directory"
    exit 1
fi

echo "============================================"
echo "Installing Dependencies"
echo "============================================"
npm install

echo ""
echo "============================================"
echo "Setup Complete! 🎉"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Copy environment file:"
echo "   cp .env.example .env.local"
echo ""
echo "2. Make sure backend is running on port 8000"
echo ""
echo "3. Start development server:"
echo "   npm run dev"
echo ""
echo "4. Open browser:"
echo "   http://localhost:5173"
echo ""
echo "============================================"
echo ""
echo "Available commands:"
echo "  npm run dev          - Start development server"
echo "  npm run build        - Create production build"
echo "  npm run preview      - Preview production build"
echo "  npm run lint         - Run ESLint"
echo "  npm run type-check   - Check TypeScript"
echo ""
echo "Documentation:"
echo "  - README.md          - Main documentation"
echo "  - QUICKSTART.md      - Quick start guide"
echo "  - SETUP.md           - Setup & deployment"
echo "  - ARCHITECTURE.md    - Technical details"
echo ""
