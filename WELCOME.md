# 👋 Welcome! Instructions for Your First Time

**Hello! Your teammate set everything up for you. Here's exactly what to do.**

## ⏱️ Time Required: 15 Minutes

---

## 📋 Prerequisites (5 Minutes)

### What You Need
Before starting, install these 3 things on your computer:

#### 1. Python 3.10 or Higher
- Go to: https://www.python.org/downloads/
- Click the big yellow "Download" button
- Run the installer
- **IMPORTANT:** Check "Add Python to PATH" during installation
- Verify: Open terminal/cmd and type: `python --version`

#### 2. Node.js 16 or Higher
- Go to: https://nodejs.org
- Click the green "LTS" button (Recommended version)
- Run the installer
- Verify: Open terminal/cmd and type: `node --version`

#### 3. Get Gemini API Key (Free!)
- Go to: https://makersuite.google.com/app/apikeys
- Click "Create API key"
- Copy the key (save it somewhere safe)
- This powers the AI insights

### Verify Everything Installed
Open a new terminal/cmd and run:
```bash
python --version    # Should show 3.10 or higher
node --version      # Should show 16 or higher
npm --version       # Should show something
```

---

## 🚀 Installation (10 Minutes)

### Step 1: Clone the Project
Open terminal/cmd and run:
```bash
git clone <repository-url>
cd weekly-report-agent
```

(Your teammate will give you the `<repository-url>`)

### Step 2: Run Verification Script
Let's check if everything is ready:

**On Windows:**
```bash
verify_setup.bat
```

**On macOS/Linux:**
```bash
bash verify_setup.sh
```

You should see [OK] next to each item.

### Step 3: Setup Backend (Terminal 1)

**Open First Terminal/CMD:**

```bash
# Navigate to backend
cd backend

# Create virtual environment (downloads Python packages)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env

# Edit .env file and add your GEMINI_API_KEY
# (Open backend/.env with text editor and add your key)

# Start the backend server
python -m uvicorn app.main:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Leave this terminal open!** ✅

### Step 4: Setup Frontend (Terminal 2)

**Open Second Terminal/CMD:**

```bash
# Navigate to frontend (from project root)
cd frontend

# Install packages
npm install

# Setup configuration
cp .env.example .env.local

# Start development server
npm run dev
```

**You should see:**
```
VITE v4.x.x ready in XXX ms
➜ Local: http://localhost:5173/
```

**Leave this terminal open!** ✅

### Step 5: Open Application

Open your web browser and go to:
```
http://localhost:5173
```

You should see a dashboard with:
- Dashboard with quick actions
- Comparison button
- Reports button  
- Chat button

**Congratulations! It's running!** 🎉

---

## 🎯 Your First Test (3 Minutes)

### Step 1: Add Test Files
Your teammate should have put some sample files in: `backend/data/weekly/`

If not, copy some Excel files there with counterparty data.

### Step 2: Run Your First Comparison
1. Click **"Comparison"** in left sidebar
2. From first dropdown, select a "Week 1" file
3. From second dropdown, select a "Week 2" file
4. Keep all settings as default
5. Check the "Generate AI Insights" box
6. Click **"Run Comparison"**
7. Wait 30-60 seconds...
8. See the results! 🎉

### Step 3: View Results
You'll see:
- Summary statistics (how many rows matched, changed, etc.)
- Detailed metrics table
- AI-generated business insights
- Movement analysis

### Step 4: Generate Report
1. Click **"Generate Report"** button
2. Choose **"Both"** (PDF and Excel)
3. Click **"Generate"**
4. Report appears in Reports page
5. Click download icon to get file

### Step 5: Chat About Results
1. Click **"Chat"** in sidebar
2. Type a question like:
   - "Show me entities with highest variance"
   - "Which metrics increased the most"
   - "List all new entities"
3. AI responds with insights!

---

## 🐛 Something Doesn't Work?

### Backend won't start

**Error: "ModuleNotFoundError"**
```bash
cd backend
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt   # Try again
```

**Error: "Address already in use" or "Port 8000"**
```bash
# Kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Frontend won't start

**Error: "command not found" or "module not found"**
```bash
cd frontend
npm cache clean --force
rm -rf node_modules
npm install
npm run dev
```

**Error: "Port 5173 already in use"**
```bash
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5173
kill -9 <PID>
```

### Files don't appear in dropdown

Put Excel files in: `backend/data/weekly/`

The backend automatically discovers files there.

### "Cannot connect to server" or "Network error"

1. Check backend is running (first terminal should show "running on http://0.0.0.0:8000")
2. Check frontend .env.local has: `VITE_API_BASE_URL=http://localhost:8000`
3. Open http://localhost:8000/docs to test backend directly

---

## 📚 Documentation

If you need more details:

1. **AFTER_PULL.md** - Quick reference (1 page)
2. **FIRST_TIME_SETUP.md** - Detailed setup (full guide)
3. **backend/README.md** - Backend documentation
4. **frontend/README.md** - Frontend documentation

---

## ✅ Verification Checklist

After setup, check:

- [ ] Backend running on http://localhost:8000
- [ ] Can see API docs at http://localhost:8000/docs
- [ ] Frontend running on http://localhost:5173
- [ ] Can see dashboard in browser
- [ ] Can see "Comparison" page
- [ ] Can see files in dropdown (if files exist in backend/data/weekly/)
- [ ] No error in browser console (F12 → Console tab)
- [ ] No error in terminal windows

---

## 📞 Need Help?

1. **Check terminal output** - Error messages are usually helpful
2. **Check browser console** - F12 → Console tab
3. **Read the troubleshooting** - Above in this file
4. **Read FIRST_TIME_SETUP.md** - More detailed explanations

---

## 🎯 What to Do Next

Once everything is running:

1. **Explore the UI** - Click around and see what's there
2. **Run a test comparison** - Follow the workflow above
3. **Read documentation** - Understand how it works
4. **Start using for real** - Replace sample data with your real data

---

## ⏱️ Time Summary

| Step | Time |
|------|------|
| Install prerequisites | 5 min |
| Setup backend | 3 min |
| Setup frontend | 2 min |
| First test | 2 min |
| **Total** | **~12 minutes** |

---

## 🎉 You're All Set!

Everything is ready to go. Follow the steps above and you'll be running the application in 15 minutes.

**Remember:**
- ✅ Keep both terminals open (backend + frontend)
- ✅ Backend runs on http://localhost:8000
- ✅ Frontend runs on http://localhost:5173
- ✅ Open http://localhost:5173 in browser

---

## 💡 Pro Tips

1. **Two Terminals** - Always keep backend and frontend in separate terminals
2. **File Locations** - Put Excel files in `backend/data/weekly/`
3. **Hot Reload** - Both backend and frontend reload when you save files
4. **Browser Console** - F12 shows helpful error messages
5. **API Docs** - http://localhost:8000/docs shows all API endpoints

---

## 🚀 Ready?

Open your terminal, follow the steps above, and you'll be analyzing reports in 15 minutes!

**Questions?** Ask your teammate or read FIRST_TIME_SETUP.md for more details.

**Let's go!** 🎉
