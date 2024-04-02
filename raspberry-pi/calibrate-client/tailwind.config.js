/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors:{
        'yellow' : '#FACC15',
        'blue' : '#3C73EF',
        'dark-blue' : '#111842',
        'grey' : '#808080',
        'red' : '#FF0000'
      }
    },
  },
  plugins: [],
}

