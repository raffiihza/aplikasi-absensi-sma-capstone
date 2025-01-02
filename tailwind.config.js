/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./webabsensi/templates/**/*.html", // All HTML files in templates folder
    "./webabsensi/static/**/*.js", // All JS files in static folder
    "./webabsensi/static/**/*.css", // Optional: CSS files if needed
  ],
  theme: {
    extend: {
      colors: {
        "custom-green": "#97B2A7",
        "hover-green": "#5E7F70",
        "sidebar-green": "#97B2A7",
      },
      // background: {
      //   "sidebar-green": "#97B2A7",
      // },
      fontFamily: {
        lato: ["Lato", "sans-serif"],
      },
    },
  },
  plugins: [],
};
