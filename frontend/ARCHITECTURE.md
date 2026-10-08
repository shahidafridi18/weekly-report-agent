# Frontend Architecture Documentation

## Overview

This is a modern React + TypeScript frontend for the Weekly Report Analysis Agent. The architecture follows best practices with clear separation of concerns, state management, and API communication.

## Architecture Layers

### 1. Presentation Layer (Components)
Located in `/src/components/`, organized by feature:

- **Layout**: Navigation and page structure
- **Comparison**: File selection and results display
- **Chat**: Messaging interface
- **Reports**: Report generation and download
- **Common**: Reusable UI components

### 2. Page Layer (Pages)
Located in `/src/pages/`, maps routes to full-page components:

- Dashboard
- ComparisonPage
- ReportsPage
- ChatPage

### 3. State Management (Redux)
Located in `/src/store/`:

```
├── store.ts                    # Store configuration
└── slices/
    ├── comparisonSlice.ts      # Comparison state
    ├── reportSlice.ts          # Report state
    ├── chatSlice.ts            # Chat state
    └── uiSlice.ts              # UI state
```

### 4. Data Layer (Services)
Located in `/src/services/index.ts`:

Defines service classes:
- `ComparisonService`: API calls for comparisons
- `ReportService`: Report generation and download
- `ChatService`: Chat messaging
- `FileService`: File listing

### 5. Utilities (Hooks, Utils, Types)

**Hooks** (`/src/hooks/`):
- Custom React hooks for business logic
- Encapsulate API calls and state management
- Examples: `useComparison`, `useChat`, `useReports`

**Utils** (`/src/utils/`):
- Formatting functions (numbers, dates, etc.)
- Constants and configuration
- API client setup

**Types** (`/src/types/`):
- TypeScript interfaces for all data structures
- Matches backend API schemas

## Data Flow

### Request Flow
```
User Input (Component)
        ↓
Event Handler
        ↓
Custom Hook
        ↓
Redux Action (dispatch)
        ↓
Redux Reducer (state update)
        ↓
API Service Call
        ↓
HTTP Request (Axios)
        ↓
Backend API
```

### Response Flow
```
Backend API Response
        ↓
API Service (parse response)
        ↓
Redux Action (dispatch with data)
        ↓
Redux Reducer (update state)
        ↓
Component Re-render (useSelector)
        ↓
UI Update
```

## State Management Strategy

### Redux Store Structure
```javascript
{
  comparison: {
    request: CompareRequest | null,
    results: ComparisonAnalysis | null,
    aiInsights: string | null,
    loading: boolean,
    error: string | null
  },
  reports: {
    reports: Report[],
    currentReport: Report | null,
    loading: boolean,
    error: string | null,
    downloadProgress: number
  },
  chat: {
    messages: ChatMessage[],
    sessionId: string | null,
    loading: boolean,
    error: string | null
  },
  ui: {
    sidebarOpen: boolean,
    notifications: Notification[],
    theme: 'light' | 'dark',
    loading: boolean
  }
}
```

### When to Use Redux vs Local State

**Use Redux for**:
- Global app state (user, auth, theme)
- Comparison results (needed across multiple pages)
- Chat history (persistent within session)
- Report list

**Use Local State for**:
- Form inputs
- UI toggles (hover, open/close)
- Temporary UI state
- Animation states

## API Integration

### API Client Setup (`/src/utils/api.ts`)

```typescript
const apiClient = new ApiClient();
// Configured with:
// - Base URL from env
// - Default timeout
// - Error handling
// - Response interceptors
```

### Service Pattern

Each domain has a service class:
```typescript
class ComparisonService {
  async compareFiles(request: CompareRequest): Promise<ComparisonResponse> {
    // Make API call
    // Handle errors
    // Return parsed data
  }
}
```

### Error Handling

- API errors caught in service layer
- Dispatched to Redux state
- Displayed in UI via error boundaries or toast notifications
- 401 errors redirect to login (when implemented)

## Component Patterns

### Functional Components
All components are functional components with hooks.

### Custom Hooks Pattern
```typescript
// Service layer
const comparisonService = new ComparisonService();

// Hook layer
export const useComparison = () => {
  const dispatch = useAppDispatch();
  const { loading, results } = useAppSelector(state => state.comparison);
  
  const runComparison = async (request: CompareRequest) => {
    dispatch(setLoading(true));
    try {
      const data = await comparisonService.compareFiles(request);
      dispatch(setResults(data));
    } catch (error) {
      dispatch(setError(error.message));
    }
  };
  
  return { loading, results, runComparison };
};

// Component layer
export const MyComponent = () => {
  const { loading, results, runComparison } = useComparison();
  // Use the hook in component
};
```

### Error Boundary
Wraps entire app to catch React errors:
```typescript
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

## Styling Architecture

### Tailwind CSS
- Utility-first CSS framework
- Configuration in `tailwind.config.js`
- Custom colors defined for brand consistency
- No custom CSS needed for most styling

### Custom Colors
```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      navy: "#24364B",      // Primary
      blue: "#315F8C",      // Secondary
      success: "#2E7D32",   // Positive
      danger: "#B3261E",    // Negative
      warning: "#B26A00",   // Caution
    }
  }
}
```

### Global Styles
In `/src/styles/index.css`:
- Tailwind directives
- Custom animations
- Utility classes
- Reset styles

## Routing Architecture

### React Router Setup
```typescript
<BrowserRouter>
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/comparison" element={<ComparisonPage />} />
    <Route path="/reports" element={<ReportsPage />} />
    <Route path="/chat" element={<ChatPage />} />
  </Routes>
</BrowserRouter>
```

### Navigation
Via Sidebar component and programmatically:
```typescript
const navigate = useNavigate();
navigate('/comparison');
```

## Form Handling

Uses `react-hook-form` for complex forms:
```typescript
const { register, handleSubmit, watch } = useForm();
```

For simple forms, local state is fine.

## Authentication (Placeholder)

Currently no authentication. When implementing:

1. Add auth slice to Redux
2. Add login/logout actions
3. Add auth guard middleware
4. Store JWT token in localStorage
5. Add token to API request headers

## Testing Strategy (Future)

When implementing tests:

1. **Unit Tests**: Test individual functions and hooks
2. **Component Tests**: Test component rendering and interactions
3. **Integration Tests**: Test API calls and Redux integration
4. **E2E Tests**: Test full user workflows

Use Vitest + React Testing Library

## Performance Considerations

### Code Splitting
Vite automatically code-splits by route.

### Lazy Loading
```typescript
const ComparisonPage = lazy(() => import('./pages/ComparisonPage'));

<Suspense fallback={<Loading />}>
  <ComparisonPage />
</Suspense>
```

### Memoization
- `useMemo` for expensive calculations
- `useCallback` for function references
- `React.memo` for component memoization

### Bundle Size
Monitor with:
```bash
npm run build  # Shows bundle size
```

## Security Best Practices

1. **Input Validation**: Always validate user inputs
2. **XSS Prevention**: React auto-escapes JSX
3. **CSRF Protection**: Use SameSite cookies
4. **API Security**: Validate all API responses
5. **Environment Secrets**: Never commit `.env.local`

## Accessibility (a11y)

Considerations for future enhancements:
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast compliance
- Screen reader support

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

IE11 not supported (uses ES6+)

## Common Patterns

### Loading State in Component
```typescript
if (loading) {
  return <Loading message="Processing..." />;
}
```

### Error Handling
```typescript
if (error) {
  return <ErrorMessage message={error} />;
}
```

### Empty State
```typescript
if (items.length === 0) {
  return <EmptyState message="No items found" />;
}
```

### Conditional Rendering
```typescript
{condition && <Component />}
{condition ? <ComponentA /> : <ComponentB />}
```

## File Naming Conventions

- **Components**: PascalCase (e.g., `ComparisonForm.tsx`)
- **Files**: camelCase (e.g., `useComparison.ts`)
- **Hooks**: Start with `use` (e.g., `useComparison`)
- **Types**: PascalCase with `Type` suffix (e.g., `ComparisonType`)

## Development Workflow

1. Create component in appropriate folder
2. Export from index file
3. Import in parent component
4. Add types in `/src/types/`
5. Add API calls to service
6. Add Redux slice if needed
7. Create hook to integrate service + Redux
8. Use hook in component
9. Add styles with Tailwind
10. Test in browser

## Build Process

```bash
npm run build
```

Vite processes:
1. TypeScript compilation
2. JSX transformation
3. Tailwind CSS compilation
4. Code bundling and minification
5. Asset optimization
6. Tree shaking

Output: Optimized `dist/` folder

## Deployment Checklist

- [ ] Environment variables configured
- [ ] API URL points to production
- [ ] Error logging configured (if used)
- [ ] Analytics configured (if used)
- [ ] Build passes type check
- [ ] Build passes linter
- [ ] All tests pass
- [ ] Bundle size acceptable
- [ ] Performance metrics good
- [ ] Security headers configured

---

This architecture provides a solid foundation for scaling the application while maintaining code quality and developer experience.
