@echo off
REM Installation script for Windows
REM Run: install.bat

echo ============================================
echo Weekly Report Agent Frontend Setup
echo ============================================
echo.

REM Check Node.js
where node >nul 2>nul
if errorlevel 1 (
    echo ERROR: Node.js is not installed
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node -v') do set NODE_VERSION=%%i
echo Node.js detected: %NODE_VERSION%
echo.

REM Check npm
where npm >nul 2>nul
if errorlevel 1 (
    echo ERROR: npm is not installed
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm -v') do set NPM_VERSION=%%i
echo npm detected: %NPM_VERSION%
echo.

REM Check package.json
if not exist "package.json" (
    echo ERROR: package.json not found
    echo Please run this script from the frontend directory
    pause
    exit /b 1
)

echo ============================================
echo Installing Dependencies
echo ============================================
call npm install

if errorlevel 1 (
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup Complete! [checkmark]
echo ============================================
echo.
echo Next steps:
echo 1. Copy environment file:
echo    copy .env.example .env.local
echo.
echo 2. Make sure backend is running on port 8000
echo.
echo 3. Start development server:
echo    npm run dev
echo.
echo 4. Open browser:
echo    http://localhost:5173
echo.
echo ============================================
echo.
echo Available commands:
echo   npm run dev          - Start development server
echo   npm run build        - Create production build
echo   npm run preview      - Preview production build
echo   npm run lint         - Run ESLint
echo   npm run type-check   - Check TypeScript
echo.
echo Documentation:
echo   - README.md          - Main documentation
echo   - QUICKSTART.md      - Quick start guide
echo   - SETUP.md           - Setup and deployment
echo   - ARCHITECTURE.md    - Technical details
echo.
pause
