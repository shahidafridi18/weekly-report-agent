# Weekly Report Analysis Agent - Frontend

A modern React + TypeScript frontend for AI-powered week-over-week report comparison and analysis.

## 🚀 Features

- **File Comparison**: Upload and compare two weekly Excel reports
- **Advanced Analysis**: 
  - Entity matching and variance detection
  - Movement bridge reconciliation
  - Zero transitions analysis
  - Major movement tracking
- **AI Insights**: Gemini-powered business insights and analysis
- **Chat Interface**: Ask questions about your data with AI chatbot
- **Report Generation**: Export results as PDF or Excel
- **Responsive Design**: Works seamlessly on desktop and mobile

## 📋 Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend API running on `http://localhost:8000`

## 🔧 Installation

1. **Clone the repository** (if not already done):
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Create environment file**:
```bash
cp .env.example .env.local
```

4. **Configure API URL** (if needed):
Edit `.env.local`:
```
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

## 🏃 Running the Application

### Development Mode
```bash
npm run dev
```
The app will be available at `http://localhost:5173`

### Production Build
```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
src/
├── components/
│   ├── Layout/           # Navbar, Sidebar, MainLayout
│   ├── Comparison/       # Comparison form and results
│   ├── Chat/            # Chat interface
│   ├── Reports/         # Report generator
│   └── common/          # Reusable UI components
├── pages/               # Page components
├── services/            # API services
├── store/              # Redux store configuration
├── hooks/              # Custom React hooks
├── types/              # TypeScript types
├── utils/              # Utility functions
├── styles/             # CSS files
└── App.tsx             # Main App component
```

## 🔑 Key Technologies

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Redux Toolkit**: State management
- **Axios**: HTTP client
- **Tailwind CSS**: Styling
- **React Router**: Navigation
- **Recharts**: Charts (ready to integrate)
- **Lucide React**: Icons
- **Vite**: Build tool

## 🌐 API Integration

The frontend communicates with the backend via these endpoints:

```
POST   /api/agent/compare          - Run comparison
POST   /api/agent/reports          - Generate report
GET    /api/agent/files            - List available files
POST   /api/agent/chat             - Send chat message
GET    /api/agent/reports/{format}/{id} - Download report
```

## 🎨 Theming

The app uses a custom color scheme inspired by FCCR:
- **Navy**: `#24364B` - Primary
- **Blue**: `#315F8C` - Secondary
- **Light Blue**: `#DCE8F2` - Accent
- **Success**: `#2E7D32` - Positive changes
- **Danger**: `#B3261E` - Negative changes
- **Warning**: `#B26A00` - Caution

Customize in `tailwind.config.js`

## 📦 Dependencies

See `package.json` for full list. Key dependencies:
- `react` & `react-dom` - UI library
- `@reduxjs/toolkit` & `react-redux` - State management
- `axios` - HTTP client
- `tailwindcss` - CSS framework
- `react-router-dom` - Routing
- `react-hot-toast` - Notifications
- `lucide-react` - Icons

## 🔒 Environment Variables

```
VITE_API_BASE_URL=http://localhost:8000    # Backend API URL
VITE_API_TIMEOUT=30000                      # Request timeout in ms
```

## 📊 Usage Workflow

1. **Dashboard**: Start here to understand available actions
2. **Comparison**: 
   - Select two files from the data/weekly folder
   - Configure key columns and thresholds
   - Click "Run Comparison"
3. **Results**: View detailed analysis, metrics, and AI insights
4. **Reports**: Generate PDF or Excel reports
5. **Chat**: Ask follow-up questions about the analysis

## 🐛 Troubleshooting

**API connection errors**:
- Verify backend is running on `http://localhost:8000`
- Check `VITE_API_BASE_URL` in `.env.local`
- Check browser console for CORS issues

**State not persisting**:
- Ensure Redux store is properly initialized
- Check browser localStorage (F12 → Application → Local Storage)

**Style issues**:
- Run `npm run build` to recompile Tailwind CSS
- Clear browser cache (Ctrl+Shift+Delete)

## 🚀 Performance Tips

- Use lazy loading for heavy components
- Enable code splitting in Vite config
- Memoize expensive computations
- Use React DevTools Profiler to identify bottlenecks

## 📝 Code Style

This project uses:
- ESLint for code linting
- Prettier for code formatting
- TypeScript for type safety

Run linter:
```bash
npm run lint
```

Type check:
```bash
npm run type-check
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run linter and type check
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check browser console for errors
4. Review Redux DevTools for state issues

## 🎯 Next Steps

- [ ] Add data export functionality
- [ ] Implement real-time collaboration
- [ ] Add advanced charting features
- [ ] Build mobile app version
- [ ] Add historical trend analysis

---

**Happy analyzing!** 🎉
