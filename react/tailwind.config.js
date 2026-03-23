/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        border: 'var(--color-border)', // slate-200 / slate-700
        input: 'var(--color-input)', // slate-200 / slate-700
        ring: 'var(--color-ring)', // emerald-500
        background: 'var(--color-background)', // slate-50 / slate-900
        foreground: 'var(--color-foreground)', // gray-800 / slate-100
        primary: {
          DEFAULT: 'var(--color-primary)', // blue-900 / blue-700
          foreground: 'var(--color-primary-foreground)', // white / slate-100
        },
        secondary: {
          DEFAULT: 'var(--color-secondary)', // blue-700 / blue-900
          foreground: 'var(--color-secondary-foreground)', // white / slate-100
        },
        accent: {
          DEFAULT: 'var(--color-accent)', // emerald-500
          foreground: 'var(--color-accent-foreground)', // white / slate-100
        },
        destructive: {
          DEFAULT: 'var(--color-destructive)', // red-600
          foreground: 'var(--color-destructive-foreground)', // white / slate-100
        },
        success: {
          DEFAULT: 'var(--color-success)', // emerald-600
          foreground: 'var(--color-success-foreground)', // white / slate-100
        },
        warning: {
          DEFAULT: 'var(--color-warning)', // amber-600
          foreground: 'var(--color-warning-foreground)', // white / slate-100
        },
        error: {
          DEFAULT: 'var(--color-error)', // red-600
          foreground: 'var(--color-error-foreground)', // white / slate-100
        },
        muted: {
          DEFAULT: 'var(--color-muted)', // slate-100 / slate-700
          foreground: 'var(--color-muted-foreground)', // gray-500 / slate-400
        },
        card: {
          DEFAULT: 'var(--color-card)', // white / slate-800
          foreground: 'var(--color-card-foreground)', // gray-800 / slate-100
        },
        popover: {
          DEFAULT: 'var(--color-popover)', // white / slate-800
          foreground: 'var(--color-popover-foreground)', // gray-800 / slate-100
        },
      },
      borderRadius: {
        sm: 'var(--radius-sm)', // 6px
        md: 'var(--radius-md)', // 10px
        lg: 'var(--radius-lg)', // 14px
        xl: 'var(--radius-xl)', // 18px
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
      },
      fontFamily: {
        heading: ['Outfit', 'sans-serif'],
        body: ['Source Sans 3', 'sans-serif'],
        caption: ['Inter', 'sans-serif'],
        data: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '112': '28rem',
      },
      transitionDuration: {
        '250': '250ms',
      },
      transitionTimingFunction: {
        'smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      maxWidth: {
        'measure': '70ch',
      },
      zIndex: {
        '800': '800',
        '900': '900',
        '1000': '1000',
        '1050': '1050',
        '1100': '1100',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('tailwindcss-animate'),
  ],
}