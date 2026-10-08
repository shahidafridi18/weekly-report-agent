# 🚀 What to Do After You Pull - Quick Reference

**For your teammate** - This is the ONLY file to read first!

## 📋 Before You Start

Your computer needs:
1. ✅ **Python 3.10+** - https://python.org/downloads
2. ✅ **Node.js 16+** - https://nodejs.org
3. ✅ **Git** - https://git-scm.com
4. ✅ **Gemini API Key** (free) - https://makersuite.google.com/app/apikeys

---

## ⚡ Quick Start (3 Commands, 5 Minutes)

### Command 1: Setup Backend (First Terminal)
```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

python -m uvicorn app.main:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Leave this terminal running!

---

### Command 2: Setup Frontend (Second Terminal)
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

**You should see:**
```
VITE v4.x.x ready in XXX ms
➜ Local: http://localhost:5173/
```

Leave this terminal running!

---

### Command 3: Open Browser
```
http://localhost:5173
```

**Done!** ✅ Application is running!

---

## 🎯 First Time Using

1. **Dashboard loads** - Click anything to explore
2. **Add test files** - Put Excel files in `backend/data/weekly/`
3. **Run Comparison**:
   - Go to "Comparison" page
   - Select two files
   - Click "Run Comparison"
   - Wait 30-60 seconds
   - See results with AI insights!
4. **Generate Reports** - Click "Generate Report" button
5. **Chat** - Go to Chat page and ask questions

---

## 🐛 If Something Goes Wrong

### Backend won't start
```bash
# Make sure you're in backend folder and venv is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then run:
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend won't start
```bash
cd frontend
npm cache clean --force
rm -rf node_modules
npm install
npm run dev
```

### Port is already in use
Kill the process using the port:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Files don't appear
Put Excel files in: `backend/data/weekly/`

---

## 📂 Project Layout

```
weekly-report-agent/
├── backend/      ← Terminal 1: Start here
├── frontend/     ← Terminal 2: Start here
└── README.md     ← Full documentation
```

---

## 📖 Documentation Files

| File | Read When |
|------|-----------|
| **FIRST_TIME_SETUP.md** | Need detailed instructions |
| **backend/README.md** | Want to understand backend |
| **frontend/README.md** | Want to understand frontend |
| **This file** | Getting started NOW |

---

## ✅ Checklist

After running the 3 commands above:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can see dashboard in browser
- [ ] Can see "Comparison" page
- [ ] Can see file dropdown with no error
- [ ] Ready to test!

---

## 🎯 Next Steps

1. **Put test files** in `backend/data/weekly/` (use sample_data/ as reference)
2. **Run comparison** - Select files and click compare
3. **View results** - See metrics and AI insights
4. **Generate report** - Export as PDF or Excel
5. **Chat** - Ask questions about the analysis

---

## 🚨 Common Mistakes

❌ Running backend and frontend in same terminal
- ✅ Use **TWO separate terminals**

❌ Not activating Python venv
- ✅ Activate it first: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)

❌ Files not in right folder
- ✅ Put Excel files in: `backend/data/weekly/`

❌ Forgot .env files
- ✅ Copy .env.example to .env (backend) and .env.local (frontend)

❌ Python/Node not installed
- ✅ Check `python --version` and `node --version`

---

## ⏱️ Time Estimates

- Installation: 5-10 minutes
- First comparison: 1 minute
- First report: 30 seconds
- All familiar: 15 minutes total

---

## 📞 Help!

If something doesn't work:

1. **Check this file** - Solutions above
2. **Check FIRST_TIME_SETUP.md** - Detailed setup guide
3. **Check your terminal output** - Read the error message
4. **Check browser console** - F12 → Console tab

---

## ✨ You're Ready!

Everything is setup. Go ahead and:

1. Open two terminals
2. Run commands above
3. Open http://localhost:5173
4. Enjoy! 🎉

**Questions?** See FIRST_TIME_SETUP.md for detailed help.
