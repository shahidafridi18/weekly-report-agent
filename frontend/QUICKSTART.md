# Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

Wait for all packages to install (~2-3 minutes depending on connection)

### Step 2: Environment Setup
```bash
cp .env.example .env.local
```

Default settings should work if backend is on `localhost:8000`

### Step 3: Start Development
```bash
npm run dev
```

Open browser to `http://localhost:5173`

## 📖 First Use

### Dashboard
- Read the overview
- Click on "Run Comparison" to get started

### Comparison Page
1. Select "Week 1" file from dropdown
2. Select "Week 2" file from dropdown
3. Adjust thresholds if needed (defaults are fine)
4. Check "Generate AI Insights" box
5. Click "Run Comparison"
6. Wait for analysis (usually 30-60 seconds)
7. View results with charts and insights

### View Reports
1. Click "Reports" in sidebar
2. Click "Generate Report" button
3. Choose format (PDF or Excel)
4. Download appears in your downloads folder

### Chat
1. Click "Chat" in sidebar
2. Ask questions like:
   - "Show me entities with highest variance"
   - "Which metrics increased the most"
   - "List all new entities"
3. Get AI-powered responses

## 🎯 Common Tasks

### Run a Different Comparison
Navigate to Comparison page → Click "New Comparison" button

### Download Previous Report
Go to Reports page → Click download icon next to report

### Clear Chat History
Refresh the page (chat doesn't persist between sessions yet)

## 🔧 Troubleshooting

### App won't load
- Check if backend is running on port 8000
- Check browser console (F12) for errors
- Kill and restart dev server: `npm run dev`

### Files don't appear
- Ensure files exist in backend's `data/weekly/` folder
- Backend needs to be running

### API errors
- Check network tab in DevTools (F12)
- Verify `VITE_API_BASE_URL` in `.env.local`
- Check backend logs for errors

## 📂 File Structure Quick Reference

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Full-page components
│   ├── services/       # API communication
│   ├── store/          # Redux state
│   ├── hooks/          # Custom React hooks
│   ├── types/          # TypeScript types
│   ├── utils/          # Utility functions
│   ├── styles/         # CSS files
│   ├── App.tsx         # Main app
│   └── main.tsx        # Entry point
├── package.json        # Dependencies
├── tsconfig.json       # TypeScript config
├── tailwind.config.js  # Tailwind CSS config
└── vite.config.ts      # Vite config
```

## 💡 Tips & Tricks

### Keyboard Shortcuts
- `Cmd/Ctrl + K`: Search for commands (if implemented)
- `Cmd/Ctrl + Shift + Delete`: Clear cache
- `F12`: Open DevTools

### Browser Extensions
Recommended:
- React DevTools
- Redux DevTools
- Network Debugger

### Performance Tips
- Use Chrome DevTools Performance tab
- Check "Slow 3G" in Network tab to test on slow connections
- Use Lighthouse for performance audits

## 🐛 Debug Mode

Enable detailed logging by adding to `main.tsx`:
```typescript
if (process.env.NODE_ENV === 'development') {
  // Add debug utilities
  window.__DEBUG__ = true;
}
```

## 🎓 Learning Resources

- [React Hooks Guide](https://react.dev/reference/react)
- [Redux Toolkit Docs](https://redux-toolkit.js.org)
- [Tailwind CSS Tutorial](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 📝 Development Checklist

Before committing code:
- [ ] No TypeScript errors: `npm run type-check`
- [ ] No linting errors: `npm run lint`
- [ ] Component renders without errors
- [ ] API calls work correctly
- [ ] UI looks good on mobile and desktop
- [ ] No console errors or warnings

## 🚀 Ready to Deploy?

### Build for Production
```bash
npm run build
```

### Test Production Build
```bash
npm run preview
```

### Deploy Options
1. **Vercel** (easiest for Vite): `npm install -g vercel && vercel`
2. **Netlify**: `netlify deploy --prod --dir=dist`
3. **Your own server**: Copy `dist/` folder to web server

## 🆘 Need Help?

1. Check console: `F12 → Console tab`
2. Check Network: `F12 → Network tab`
3. Check Redux: `F12 → Redux DevTools`
4. Read error messages carefully
5. Check ARCHITECTURE.md for deep dives
6. Check SETUP.md for detailed setup

## 🎉 You're All Set!

Start by:
1. Going to Dashboard
2. Running your first comparison
3. Exploring the results
4. Asking questions in chat

Happy analyzing! 📊
