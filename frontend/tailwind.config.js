import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: "#24364B",
        blue: "#315F8C",
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
