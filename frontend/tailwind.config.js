/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1A73E8', // Horizon Blue
          dark: '#1557B0',
        },
        surface: '#FFFFFF', // Paper White
        background: '#F8F9FA', // Cloud Gray
        text: {
          primary: '#202124', // Midnight Onyx
          secondary: '#5F6368',
        },
        accent: '#FB8C00', // Sunset Orange
        dark: {
          background: '#121212',
          surface: '#1E1E1E',
          text: '#E8EAED',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}
