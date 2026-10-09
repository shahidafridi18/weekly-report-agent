# Weekly Report Analysis Agent - Complete Setup Guide

**This is your first-time setup guide.** Follow these steps exactly to get everything running.

## 📋 Prerequisites (Install Before Starting)

Before you start, ensure you have these installed on your machine:

### Required Software
1. **Python 3.10+**
   - Download from: https://www.python.org/downloads/
   - During installation, **CHECK "Add Python to PATH"**
   - Verify: Open terminal/cmd and run `python --version`

2. **Node.js 16+**
   - Download from: https://nodejs.org
   - Recommend: LTS version
   - Verify: Open terminal/cmd and run `node --version` and `npm --version`

3. **Git**
   - Download from: https://git-scm.com
   - Verify: Open terminal/cmd and run `git --version`

4. **Gemini API Key** (for AI insights)
   - Get from: https://makersuite.google.com/app/apikeys
   - Save it somewhere safe (you'll need it later)

---

## 🚀 Quick Start (3 Minutes)

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd weekly-report-agent
```

### Step 2: Setup Backend (First Terminal)
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start backend server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on: **http://localhost:8000**

### Step 3: Setup Frontend (Second Terminal)
```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

### Step 4: Open Application
Open browser: **http://localhost:5173**

You're ready to use the app! 🎉

---

## 📁 Project Structure

```
weekly-report-agent/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app
│   │   ├── api/            # API endpoints
│   │   ├── analysis/       # Analysis engines
│   │   ├── reporting/      # Report generation
│   │   ├── insights/       # AI insights
│   │   └── ...
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Environment template
│   └── venv/               # Python virtual environment
│
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── store/          # Redux state
│   │   ├── hooks/          # Custom hooks
│   │   └── ...
│   ├── package.json        # npm dependencies
│   ├── .env.example        # Environment template
│   └── node_modules/       # npm packages
│
├── sample_data/            # Sample Excel files for testing
├── .gitignore
└── README.md
```

---

## 🔧 Detailed Setup Instructions

### Backend Setup (Python/FastAPI)

#### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
```

#### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- FastAPI - Web framework
- Uvicorn - ASGI server
- openpyxl - Excel handling
- pandas - Data processing
- reportlab - PDF generation
- google-generativeai - Gemini API
- pydantic - Data validation
- python-multipart - File uploads

#### 4. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env and add:
# GEMINI_API_KEY=your_api_key_here
# Data folder paths
# API configuration
```

#### 5. Start Backend Server
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

#### 6. Test Backend
Open browser: **http://localhost:8000/docs**

You'll see interactive API documentation (Swagger UI).

---

### Frontend Setup (Node.js/React)

#### 1. Install Dependencies
```bash
cd frontend
npm install
```

This takes 2-5 minutes. Wait for it to complete.

#### 2. Configure Environment
```bash
# Copy template
cp .env.example .env.local

# Edit .env.local and verify:
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

#### 3. Start Development Server
```bash
npm run dev
```

You should see:
```
  VITE v4.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

#### 4. Open Application
Click the URL or open: **http://localhost:5173**

---

## 📊 First-Time Workflow

### 1. Login / Access Dashboard
- ✅ Application loads on http://localhost:5173
- ✅ You see dashboard with quick actions
- ✅ No login required (implement later if needed)

### 2. Prepare Test Data
- ✅ Place Excel files in `backend/data/weekly/` folder
- ✅ Files should have counterparty data (SIREN, Unique Identifier, metrics)
- ✅ Use `sample_data/` as reference
- ✅ Or upload files in UI (if implemented)

### 3. Run Your First Comparison
1. Go to **Comparison** page
2. Select **"Week 1" file** from dropdown
3. Select **"Week 2" file** from dropdown
4. Configure options:
   - Key columns: `SIREN, Unique Identifier`
   - Movement threshold: `20.0`
   - Minimum absolute change: `0.0`
   - Check "Generate AI Insights"
5. Click **"Run Comparison"**
6. Wait 30-60 seconds
7. View results with AI insights

### 4. Generate Reports
1. Click **"Generate Report"** button
2. Choose format: **PDF** or **Excel**
3. Click **"Generate"**
4. Download report

### 5. Chat About Results
1. Go to **Chat** page
2. Ask questions like:
   - "Show me entities with highest variance"
   - "Which metrics increased the most"
   - "List new entities"
3. Get AI-powered responses

---

## 🐛 Troubleshooting

### Port Already in Use

**Backend (8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**Frontend (5173):**
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5173
kill -9 <PID>
```

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Check for syntax errors
python -m py_compile app/main.py
```

### Frontend Won't Start

```bash
# Check Node version
node --version  # Should be 16+
npm --version   # Should be 7+

# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

### API Connection Error

```bash
# Check backend is running
# Go to http://localhost:8000/health

# Check frontend .env.local
cat .env.local
# Should show: VITE_API_BASE_URL=http://localhost:8000

# Check network in browser (F12 → Network tab)
```

### Files Not Appearing

```bash
# Verify backend folder path
ls backend/data/weekly/
# Should show your Excel files

# Check backend logs
# Backend console should show file discovery
```

---

## 📚 Documentation Files

Once setup, read these in order:

1. **backend/README.md** - Backend documentation
2. **frontend/README.md** - Frontend documentation
3. **frontend/QUICKSTART.md** - Quick reference
4. **frontend/ARCHITECTURE.md** - How frontend works
5. **backend/requirements.txt** - What's installed

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend running on http://localhost:8000
- [ ] Backend API docs available at http://localhost:8000/docs
- [ ] Frontend running on http://localhost:5173
- [ ] Dashboard page loads
- [ ] Files visible in Comparison page dropdown
- [ ] Can run a comparison
- [ ] Results display with AI insights
- [ ] Can generate reports
- [ ] Chat interface responds

---

## 🎯 Common First-Time Issues

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: No module named 'fastapi'" | Activate venv: `venv\Scripts\activate` then `pip install -r requirements.txt` |
| "npm: command not found" | Install Node.js from https://nodejs.org |
| "python: command not found" | Install Python from https://python.org and add to PATH |
| Port 8000 already in use | Close other app or kill process (see troubleshooting) |
| Blank page on frontend | Check browser console (F12) and backend logs |
| Files not in dropdown | Put Excel files in `backend/data/weekly/` |
| API 404 errors | Verify backend running and check VITE_API_BASE_URL |

---

## 🚀 Next Steps

### After Initial Setup

1. **Test with sample data**
   - Copy files from `sample_data/` to `backend/data/weekly/`
   - Run a comparison

2. **Understand the workflow**
   - Read backend README
   - Read frontend README

3. **Customize for your needs**
   - Add more file sources
   - Customize API parameters
   - Add authentication

4. **Deploy to production**
   - See backend README for deployment
   - See frontend README for deployment

---

## 📞 Getting Help

If something doesn't work:

1. **Check this guide** - See troubleshooting section
2. **Check logs** - Backend logs show errors
3. **Check browser console** - F12 → Console tab
4. **Check network** - F12 → Network tab
5. **Check documentation** - backend/README.md, frontend/README.md

---

## 🎓 Learning Resources

- **Backend**: [FastAPI Docs](https://fastapi.tiangolo.com)
- **Frontend**: [React Docs](https://react.dev)
- **API**: [Swagger UI at http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📝 Environment Variables Reference

### Backend (.env)
```
GEMINI_API_KEY=your_api_key_here
DATA_FOLDER=./data/weekly
OUTPUT_FOLDER=./output
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

---

## ✨ You're Ready!

Everything is set up. Start from **Quick Start** section and you'll be analyzing reports in minutes.

**Questions?** Check the troubleshooting section or read the documentation files.

**Ready?** Let's go! 🚀
