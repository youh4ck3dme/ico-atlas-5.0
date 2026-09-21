/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '5rem',
        '2xl': '6rem',
      },
    },
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Inter', 'system-ui', 'sans-serif'], // Or 'Playfair Display' if you want a serif heading
      },
      colors: {
        slovak: {
          blue: '#0B4EA2', // Official Slovak Blue
          red: '#EE1C25',  // Official Slovak Red
          white: '#FFFFFF',
          dark: '#0A0A0A'
        }
      },
      animation: {
        'fade-in': 'fade-in 0.3s ease-out',
      }
    },
  },
  plugins: [],
};

