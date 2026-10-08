# npm Dependencies Summary

This file documents all npm packages installed for the frontend.

## Installation Command
```bash
npm install
```

## Core Dependencies

### React & DOM
- **react** (18.2.0) - UI library
- **react-dom** (18.2.0) - React DOM rendering

### State Management
- **@reduxjs/toolkit** (1.9.7) - Redux state management
- **react-redux** (8.1.3) - React bindings for Redux

### Routing
- **react-router-dom** (6.20.0) - Client-side routing

### HTTP Client
- **axios** (1.6.2) - Promise-based HTTP client

### UI & Styling
- **tailwindcss** (3.4.0) - Utility-first CSS framework
- **lucide-react** (0.294.0) - Icon library

### Charts & Visualization
- **recharts** (2.10.3) - React charting library (ready to use)

### Notifications
- **react-hot-toast** (2.4.1) - Toast notifications

### Forms
- **react-hook-form** (7.49.1) - Performant form library
- **@hookform/resolvers** (3.3.4) - Form validation resolvers

### Utilities
- **clsx** (2.0.0) - Conditional className utility
- **date-fns** (2.30.0) - Date utility library

## Development Dependencies

### TypeScript
- **typescript** (5.3.3) - TypeScript compiler

### Build Tool
- **vite** (5.0.8) - Next-generation frontend build tool
- **@vitejs/plugin-react** (4.2.1) - React plugin for Vite

### Styling
- **autoprefixer** (10.4.17) - PostCSS plugin for vendor prefixes
- **postcss** (8.4.32) - CSS transformation tool

### Linting
- **eslint** (8.56.0) - JavaScript linter
- **eslint-plugin-react-hooks** (4.6.0) - React Hooks linting
- **eslint-plugin-react-refresh** (0.4.5) - Vite HMR linting

### Type Definitions
- **@types/react** (18.2.43) - React type definitions
- **@types/react-dom** (18.2.17) - React DOM type definitions

## Optional Dependencies (Not Installed Yet)

### Testing (when ready)
```bash
npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
```

### Debugging
- redux-devtools-extension (already supports DevTools extension)

### Performance Monitoring
```bash
npm install web-vitals
```

## Version Management

Keep packages updated:
```bash
npm outdated          # Check outdated packages
npm update            # Update to latest compatible versions
npm audit            # Check for security vulnerabilities
npm audit fix        # Fix security issues
```

## Lock File

Always commit `package-lock.json` to version control to ensure consistent installs:
```bash
git add package-lock.json
git commit -m "Update dependencies"
```

## Installation Notes

### Size
- `node_modules/` folder: ~500MB (normal for Node.js projects)
- Build output: ~300KB (gzipped)

### Installation Time
- First install: 2-5 minutes (depends on connection)
- Updates: 30 seconds - 2 minutes

### Requirements
- Node.js 16.x or higher
- npm 7.x or higher
- ~500MB free disk space

## Dependency Tree

Key relationships:
```
react-redux → @reduxjs/toolkit
react-router-dom → react
axios → (no dependencies)
tailwindcss → postcss, autoprefixer
recharts → react
react-hook-form → (minimal)
```

## Scripts Using Dependencies

```json
{
  "dev": "vite",                          // Uses Vite
  "build": "tsc && vite build",           // Uses TypeScript & Vite
  "preview": "vite preview",              // Uses Vite
  "lint": "eslint src --ext ts,tsx",      // Uses ESLint
  "type-check": "tsc --noEmit"            // Uses TypeScript
}
```

## Updating Strategies

### Minor Updates (Safe)
```bash
npm update
```

### Major Version Updates (Careful)
Check changelog before:
```bash
npm view [package-name] versions
npm install [package-name]@[version]
```

### Security Updates
```bash
npm audit
npm audit fix
```

## Production Optimization

When building for production:
1. Tree-shaking removes unused code
2. Code splitting by route
3. Asset compression
4. CSS purging via Tailwind

Result: ~300KB gzipped for the entire app

## Dependency Security

All packages in `package.json` are:
- ✅ Actively maintained
- ✅ Widely used in production
- ✅ Regularly audited for vulnerabilities
- ✅ Compatible with each other

Run security check:
```bash
npm audit
```

---

**Total Dependencies**: ~20 direct + ~100 transitive
**Last Updated**: 2024-01-08
