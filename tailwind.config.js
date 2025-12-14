/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./resources/**/*.blade.php",
    "./resources/**/*.js",
    "./resources/**/*.vue",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Slovak Enterprise Luxury Palette
        tatra: {
          navy: '#0B1E3D',
          50: '#E8EBF0',
          100: '#D1D8E1',
          200: '#A3B0C3',
          300: '#7589A5',
          400: '#476187',
          500: '#0B1E3D',
          600: '#091831',
          700: '#071225',
          800: '#050C19',
          900: '#02060C',
        },
        slovak: {
          crimson: '#DC143C',
          50: '#FDE8EC',
          100: '#FBD1D9',
          200: '#F7A3B3',
          300: '#F3758D',
          400: '#EF4767',
          500: '#DC143C',
          600: '#B01030',
          700: '#840C24',
          800: '#580818',
          900: '#2C040C',
        },
        porcelain: {
          white: '#F8F9FA',
          50: '#FFFFFF',
          100: '#F8F9FA',
          200: '#E9ECEF',
          300: '#DEE2E6',
          400: '#CED4DA',
          500: '#ADB5BD',
          600: '#6C757D',
          700: '#495057',
          800: '#343A40',
          900: '#212529',
        },
        matte: {
          black: '#050505',
          900: '#050505',
          800: '#0A0A0A',
          700: '#141414',
          600: '#1E1E1E',
          500: '#282828',
          400: '#3C3C3C',
          300: '#505050',
          200: '#646464',
          100: '#787878',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['SF Pro Display', 'Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        // Glass morphism shadows
        'glass': '0 8px 32px 0 rgba(11, 30, 61, 0.1)',
        'glass-sm': '0 4px 16px 0 rgba(11, 30, 61, 0.08)',
        'glass-lg': '0 16px 48px 0 rgba(11, 30, 61, 0.15)',
        'glass-xl': '0 24px 64px 0 rgba(11, 30, 61, 0.2)',
        'crimson-glow': '0 0 20px rgba(220, 20, 60, 0.3)',
        'crimson-glow-lg': '0 0 40px rgba(220, 20, 60, 0.4)',
        // Dark mode variants
        'glass-dark': '0 8px 32px 0 rgba(0, 0, 0, 0.3)',
        'glass-dark-sm': '0 4px 16px 0 rgba(0, 0, 0, 0.2)',
        'glass-dark-lg': '0 16px 48px 0 rgba(0, 0, 0, 0.4)',
        'glass-dark-xl': '0 24px 64px 0 rgba(0, 0, 0, 0.5)',
      },
      backdropBlur: {
        xs: '2px',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-down': 'slideDown 0.4s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'shimmer': 'shimmer 2s linear infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-1000px 0' },
          '100%': { backgroundPosition: '1000px 0' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'shimmer-gradient': 'linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent)',
      },
    },
  },
  plugins: [],
}
