# Installation & Deployment Guide

## Prerequisites
- Node.js 16+ installed
- npm or yarn package manager
- Backend API running (port 8000)

## Step 1: Setup Frontend

### Install Node Dependencies
```bash
cd frontend
npm install
```

This will install all packages defined in `package.json`:
- React & React-DOM
- Redux & React-Redux
- React Router
- Axios
- Tailwind CSS
- TypeScript
- And more (see package.json for complete list)

## Step 2: Environment Configuration

### Create .env.local
```bash
cp .env.example .env.local
```

### Edit .env.local
```ini
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

## Step 3: Development

### Start Development Server
```bash
npm run dev
```

Server runs at: `http://localhost:5173`

Features:
- Hot module replacement (HMR)
- Proxy to backend API
- Automatic reload on file changes

### Build for Production
```bash
npm run build
```

Output: `dist/` folder (ready to deploy)

### Preview Production Build
```bash
npm run preview
```

## Deployment Options

### Option 1: Vercel (Recommended for React/Vite)
```bash
npm install -g vercel
vercel
```

### Option 2: Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

### Option 3: Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Option 4: Traditional Web Server (nginx)
```bash
npm run build
# Copy dist/ to web server root
```

## Project Structure Details

### `/src/components/`
Reusable React components organized by feature:
- `Layout/`: Main layout components (Navbar, Sidebar)
- `Comparison/`: Comparison form and results display
- `Chat/`: Chat interface component
- `Reports/`: Report generation and history
- `common/`: Shared UI components (Button, Modal, Loading, etc.)

### `/src/pages/`
Page-level components for routing:
- `Dashboard.tsx`: Home page
- `ComparisonPage.tsx`: Comparison workflow
- `ReportsPage.tsx`: Report management
- `ChatPage.tsx`: Chat interface

### `/src/services/`
API service layer:
- `index.ts`: Centralized API client and service functions
- Uses Axios for HTTP requests
- Handles error responses

### `/src/store/`
Redux state management:
- `store.ts`: Store configuration
- `slices/`: Redux slices for different features
  - `comparisonSlice.ts`: Comparison state
  - `reportSlice.ts`: Report state
  - `chatSlice.ts`: Chat messages
  - `uiSlice.ts`: UI state (sidebar, theme, notifications)

### `/src/hooks/`
Custom React hooks:
- `useComparison.ts`: Handle comparison logic
- `useChat.ts`: Handle chat logic
- `useReports.ts`: Handle report logic
- `useFiles.ts`: Fetch available files
- `useRedux.ts`: Typed Redux hooks
- `useLocalStorage.ts`: Persistent storage

### `/src/types/`
TypeScript type definitions:
- `index.ts`: All shared types and interfaces
- Matches backend API response schemas

### `/src/utils/`
Utility functions:
- `formatters.ts`: Number, date, and text formatting
- `constants.ts`: Application constants
- `api.ts`: Axios instance configuration

### `/src/styles/`
Styling:
- `index.css`: Global styles and Tailwind directives

## Workflow: From User Input to Display

### Comparison Flow
1. User selects files on ComparisonPage
2. ComparisonForm collects parameters
3. Form submission calls `useComparison.runComparison()`
4. Hook dispatches `setLoading(true)` to Redux
5. API service calls `/api/agent/compare`
6. Backend processes and returns analysis
7. Results dispatched to Redux store
8. ComparisonResults component re-renders with new data
9. MetricsTable displays detailed metrics
10. User can generate reports or ask chat questions

### Chat Flow
1. User types message in ChatInterface
2. `useChat.sendMessage()` is called
3. Message immediately added to local state
4. User message displayed in chat
5. API call to `/api/agent/chat` made
6. Loading indicator shown while waiting
7. Assistant response received
8. Assistant message added to state
9. Chat scrolls to bottom automatically

### Report Flow
1. User clicks "Generate Report" in ComparisonResults
2. ReportGenerator collects format selection
3. Calls `/api/agent/reports` with format
4. Report created and stored with unique ID
5. Report ID added to Redux reports list
6. User can download via `/api/agent/reports/{format}/{id}`
7. File downloaded to user's computer
8. Report also appears in ReportHistory

## Data Flow Architecture

```
User Interface (React Components)
        ↓
Custom Hooks (useComparison, useChat, etc.)
        ↓
Redux Store (State Management)
        ↓
API Services (Axios Client)
        ↓
Backend API (FastAPI)
        ↓
Database / File System
```

## Common Tasks

### Add New API Endpoint

1. Add to `src/services/index.ts`:
```typescript
async myNewFunction(): Promise<MyType> {
  const response = await apiClient.post<MyType>('/api/endpoint', data);
  return response.data;
}
```

2. Create hook in `src/hooks/`:
```typescript
export const useMyFeature = () => {
  const dispatch = useAppDispatch();
  const myHook = async (data) => {
    try {
      const result = await service.myNewFunction(data);
      dispatch(setMyState(result));
    } catch (error) {
      dispatch(setError(error.message));
    }
  };
  return { myHook };
};
```

3. Use in component:
```typescript
const { myHook } = useMyFeature();
```

### Add New Redux Slice

1. Create `src/store/slices/myFeatureSlice.ts`
2. Add to store configuration in `src/store/store.ts`
3. Create hook to access slice
4. Use in components with `useAppSelector` and `useAppDispatch`

### Style a Component

Use Tailwind CSS classes:
```tsx
<div className="bg-white rounded-lg shadow-md p-6">
  <h1 className="text-2xl font-bold text-navy">Title</h1>
  <p className="text-dark-grey">Description</p>
</div>
```

Custom colors defined in `tailwind.config.js`

## Debugging

### Browser DevTools
- React DevTools: Inspect components and hooks
- Redux DevTools: Time-travel debugging
- Network tab: Monitor API requests

### Console Logs
```typescript
console.log('State:', state);
console.error('Error:', error);
```

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

## Performance Optimization

### Code Splitting
Already configured in Vite. Routes are automatically code-split.

### Memoization
```typescript
import { useMemo, useCallback } from 'react';

const memoizedValue = useMemo(() => expensiveFunction(), [dependency]);
const memoizedCallback = useCallback(() => doSomething(), [dependency]);
```

### React.memo for Components
```typescript
export const MyComponent = React.memo(({ prop }) => (
  <div>{prop}</div>
));
```

## Security Considerations

1. **API Authentication**: Add JWT tokens to requests
2. **CORS**: Configure on backend for production domain
3. **Input Validation**: Validate user inputs before API calls
4. **XSS Prevention**: React automatically escapes JSX
5. **CSRF**: Use SameSite cookies

## Testing (Future Enhancement)

When ready to add tests:
```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5173 already in use | Kill process: `lsof -i :5173` then `kill -9 <PID>` |
| API 404 errors | Verify backend URL in .env.local |
| Styles not loading | Clear `.next` or `dist` folder and rebuild |
| Redux not working | Check Redux DevTools browser extension |
| Build fails | Delete `node_modules` and `package-lock.json`, then `npm install` |

## Support & Resources

- [React Docs](https://react.dev)
- [Redux Toolkit Docs](https://redux-toolkit.js.org)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [Vite Docs](https://vitejs.dev)
- [TypeScript Docs](https://www.typescriptlang.org)
