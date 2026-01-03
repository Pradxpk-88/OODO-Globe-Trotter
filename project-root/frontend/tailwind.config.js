/** @type {import('tailwindcss').config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: "#1a1a1a",
          card: "#2a2a2a",
          text: "#ffffff",
          accent: "#3b82f6",
        },
      },
    },
  },
  plugins: [],
};