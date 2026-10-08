@echo off
REM Automated setup verification script for Windows
REM Run this after pulling to check if everything is setup correctly

setlocal enabledelayedexpansion

echo ========================================
echo Weekly Report Agent - Setup Verification
echo ========================================
echo.

set MISSING=0

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
  echo [X] Python NOT found
  set MISSING=1
) else (
  for /f "tokens=*" %%i in ('python --version') do echo [OK] %%i
)

echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
  echo [X] Node.js NOT found
  set MISSING=1
) else (
  for /f "tokens=*" %%i in ('node --version') do echo [OK] Node %%i
)

echo Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
  echo [X] npm NOT found
  set MISSING=1
) else (
  for /f "tokens=*" %%i in ('npm --version') do echo [OK] npm %%i
)

echo Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
  echo [X] Git NOT found
  set MISSING=1
) else (
  for /f "tokens=*" %%i in ('git --version') do echo [OK] %%i
)

echo.
echo Checking Backend...

if exist "backend" (
  echo [OK] Backend folder exists
  
  if exist "backend\requirements.txt" (
    echo [OK] requirements.txt found
  ) else (
    echo [X] requirements.txt missing
  )
  
  if exist "backend\.env" (
    echo [OK] .env file found
  ) else (
    echo [WARN] .env file missing - run: copy backend\.env.example backend\.env
  )
) else (
  echo [X] Backend folder not found
  set MISSING=1
)

echo.
echo Checking Frontend...

if exist "frontend" (
  echo [OK] Frontend folder exists
  
  if exist "frontend\package.json" (
    echo [OK] package.json found
  ) else (
    echo [X] package.json missing
  )
  
  if exist "frontend\.env.local" (
    echo [OK] .env.local file found
  ) else (
    echo [WARN] .env.local file missing - run: copy frontend\.env.example frontend\.env.local
  )
) else (
  echo [X] Frontend folder not found
  set MISSING=1
)

echo.
echo ========================================
echo Setup Verification Complete!
echo ========================================
echo.

if %MISSING% equ 0 (
  echo All prerequisites found!
) else (
  echo Some prerequisites are missing. Please install them.
)

echo.
echo Next steps:
echo.
echo 1. Setup Backend:
echo    cd backend
echo    python -m venv venv
echo    venv\Scripts\activate
echo    pip install -r requirements.txt
echo    copy .env.example .env
echo    REM Edit .env and add GEMINI_API_KEY
echo    python -m uvicorn app.main:app --reload --port 8000
echo.
echo 2. Setup Frontend (in another terminal):
echo    cd frontend
echo    npm install
echo    copy .env.example .env.local
echo    npm run dev
echo.
echo 3. Open browser: http://localhost:5173
echo.

pause
