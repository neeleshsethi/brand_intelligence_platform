/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        pfizer: {
          blue: '#0093D0',
          'blue-dark': '#00568C',
          'blue-light': '#5CB8E6',
          gray: '#58595B',
          'gray-light': '#E6E7E8',
        },
      },
    },
  },
  plugins: [],
}
