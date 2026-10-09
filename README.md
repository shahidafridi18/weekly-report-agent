# Weekly Report Analysis Agent

Complete AI-powered week-over-week report comparison and analysis system.

## 🎯 What This Does

Compares two weekly Excel reports (previous vs current), automatically:
- Matches counterparties by key columns
- Identifies new and removed entities
- Detects variance and major movements
- Generates AI business insights (via Gemini)
- Creates professional PDF and Excel reports
- Provides chat interface for follow-up questions

## 🚀 Quick Start (5 Minutes)

### First Time Setup?
👉 **Read: [FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md)**

All detailed instructions for first-time installation.

### Already Have Prerequisites Installed?

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt   # First time only
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install                       # First time only
npm run dev
```

**Open Browser:** http://localhost:5173

---

## 📂 Project Structure

```
weekly-report-agent/
├── backend/              # FastAPI + Python
│   ├── app/
│   │   ├── main.py      # FastAPI application
│   │   ├── api/         # REST endpoints
│   │   ├── analysis/    # Analysis engines
│   │   ├── reporting/   # Report generation
│   │   ├── insights/    # AI integration
│   │   └── ...
│   ├── requirements.txt # Python packages
│   ├── .env.example     # Config template
│   └── README.md        # Backend docs
│
├── frontend/            # React + TypeScript
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API layer
│   │   └── ...
│   ├── package.json    # npm packages
│   ├── .env.example    # Config template
│   └── README.md       # Frontend docs
│
└── FIRST_TIME_SETUP.md # ← Start here!
```

---

## 📋 System Requirements

- **Python 3.10+**
- **Node.js 16+**
- **Git**
- **Gemini API Key** (free: https://makersuite.google.com/app/apikeys)

---

## 🎯 How to Use (Workflow)

### 1. Prepare Data
Place two Excel files in `backend/data/weekly/`:
- Week 1 report (e.g., `week1.xlsx`)
- Week 2 report (e.g., `week2.xlsx`)

Each file should have:
- Key columns: SIREN, Unique Identifier
- Metric columns: Gross CE, Net CE, CVA Balance, etc.

### 2. Run Comparison
1. Go to http://localhost:5173
2. Click "Comparison" in sidebar
3. Select Week 1 and Week 2 files
4. Configure thresholds (defaults fine)
5. Check "Generate AI Insights"
6. Click "Run Comparison"

### 3. View Results
- Summary statistics
- Detailed metrics table
- Movement bridge analysis
- AI-generated business insights
- Major movements and variances
- New and removed entities

### 4. Generate Report
- Click "Generate Report"
- Choose PDF or Excel
- Download

### 5. Chat About Results
- Click "Chat" in sidebar
- Ask questions about the analysis
- Get AI-powered responses

---

## 🔧 Configuration

### Backend (.env)
Create `backend/.env` from `backend/.env.example`:
```bash
GEMINI_API_KEY=your_api_key_here
DATA_FOLDER=./data/weekly
OUTPUT_FOLDER=./output
```

### Frontend (.env.local)
Create `frontend/.env.local` from `frontend/.env.example`:
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

---

## 📊 Technology Stack

### Backend
- **FastAPI** - Web framework
- **Pandas** - Data processing
- **openpyxl** - Excel handling
- **reportlab** - PDF generation
- **Google Generative AI** - Gemini integration

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Redux Toolkit** - State management
- **Tailwind CSS** - Styling
- **Vite** - Build tool

---

## 🌐 API Endpoints

### Comparison
- `POST /api/agent/compare` - Run comparison
- `POST /api/agent/analyze` - Analyze single file
- `POST /api/agent/reports` - Generate report

### Chat
- `POST /api/agent/chat` - Send message

### Files
- `GET /api/agent/files` - List available files
- `GET /api/agent/reports/{format}/{id}` - Download report

Full API docs: http://localhost:8000/docs

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **FIRST_TIME_SETUP.md** | Complete first-time setup guide |
| **backend/README.md** | Backend features and API |
| **backend/requirements.txt** | Python dependencies |
| **frontend/README.md** | Frontend features |
| **frontend/QUICKSTART.md** | Frontend quick start |
| **frontend/ARCHITECTURE.md** | Frontend architecture |

---

## ⚙️ Available Commands

### Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000  # Dev server
python create_sample_data.py                         # Generate test data
pytest                                               # Run tests
```

### Frontend
```bash
cd frontend
npm run dev          # Start dev server
npm run build        # Production build
npm run preview      # Preview build
npm run lint         # Check code
npm run type-check   # Check types
```

---

## 🚀 Deployment

### Backend
See `backend/README.md` for:
- Docker deployment
- AWS/GCP deployment
- Traditional server deployment

### Frontend
See `frontend/README.md` for:
- Vercel deployment
- Netlify deployment
- Docker deployment

---

## 🐛 Troubleshooting

### Backend won't start
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
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

### Port already in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Files not appearing
Place Excel files in `backend/data/weekly/` directory.

See `FIRST_TIME_SETUP.md` for more troubleshooting.

---

## 🎓 First Time Setup Path

1. **Read** `FIRST_TIME_SETUP.md` (this will take 10 minutes)
2. **Follow** the Quick Start section
3. **Verify** all services running
4. **Use** the workflow above

---

## 📝 Key Features

✅ **Automatic Entity Matching** - Match counterparties across reports
✅ **Variance Detection** - Identify metrics that changed
✅ **AI Insights** - Gemini-powered business analysis
✅ **Multiple Reports** - PDF and Excel formats
✅ **Chat Interface** - Ask questions about results
✅ **Responsive UI** - Works on desktop and mobile
✅ **Type Safe** - Full TypeScript support
✅ **Production Ready** - Can deploy immediately

---

## 🔑 Environment Variables Needed

### Before Starting
1. Get Gemini API Key from: https://makersuite.google.com/app/apikeys
2. Copy `backend/.env.example` to `backend/.env`
3. Add your API key
4. Copy `frontend/.env.example` to `frontend/.env.local`

---

## 📞 Support

1. **First time?** Read `FIRST_TIME_SETUP.md`
2. **Backend issues?** Read `backend/README.md`
3. **Frontend issues?** Read `frontend/README.md`
4. **Check troubleshooting** in each README

---

## ✨ Ready to Start?

👉 **Next Step: Read [FIRST_TIME_SETUP.md](FIRST_TIME_SETUP.md)**

Everything you need to get running in 5 minutes! 🚀
