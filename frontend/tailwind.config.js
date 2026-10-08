import type ,{ Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: "#24364B",
        blue: {
          DEFAULT: "#315F8C",
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
        },
        "light-blue": "#DCE8F2",
        "pale-blue": "#F3F7FA",
        "light-grey": "#F2F2F2",
        "mid-grey": "#D4D8DC",
        "dark-grey": "#495057",
        text: "#20252A",
        success: "#2E7D32",
        danger: "#B3261E",
        warning: "#B26A00",
      },
      spacing: {
        '128': '32rem',
      },
    },
  },
  plugins: [],
}
export default config
