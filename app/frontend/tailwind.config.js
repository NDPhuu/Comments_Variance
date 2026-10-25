/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          950: "#061f3a",
          900: "#0b1420",
          800: "#16212e",
          700: "#243242",
          600: "#35465a",
        },
        // Dải xanh BW — cùng giá trị với landing (--blue, --blue-text, --blue-deep, --blue-night)
        accent: {
          DEFAULT: "#0F62B3",
          50: "#EEF3F8",
          100: "#D7E5F4",
          200: "#B3CDE8",
          300: "#7FABD6",
          400: "#3B82C4",
          500: "#0F62B3",
          600: "#0B4F92",
          700: "#0A3A6B",
          800: "#072C52",
        },
        surface: {
          0: "#FFFFFF",
          50: "#F6F9FC",
          100: "#EEF3F8",
          200: "#DBE5EF",
          300: "#C9D6E4",
          400: "#8496A9",
          500: "#4A5666",
        },
        status: {
          verified: "#07734A",
          "verified-bg": "#E8F5EF",
          "verified-ring": "#A9D9C3",
          flagged: "#C3271C",
          "flagged-bg": "#FDECEA",
          "flagged-ring": "#F3BDB7",
          warning: "#B26A00",
          "warning-bg": "#FDF3E3",
          "warning-ring": "#F0D4A3",
          abstained: "#B26A00",
          "abstained-bg": "#FDF3E3",
          "abstained-ring": "#F0D4A3",
        },
      },
      fontFamily: {
        // Một phông duy nhất. `font-mono` chỉ còn để đánh dấu số, xem .font-mono trong index.css.
        sans: ["Archivo", "system-ui", "sans-serif"],
        mono: ["Archivo", "system-ui", "sans-serif"],
      },
      // Góc vuông như landing. `rounded-full` giữ nguyên cho chấm tròn.
      borderRadius: {
        none: "0",
        sm: "0",
        DEFAULT: "0",
        md: "0",
        lg: "0",
        xl: "0",
        "2xl": "0",
        "3xl": "0",
      },
      // Không đổ bóng ở trạng thái nghỉ — phân tầng bằng viền và nền.
      boxShadow: {
        none: "none",
        sm: "none",
        DEFAULT: "none",
        md: "none",
        lg: "none",
        xl: "none",
        card: "none",
        "card-hover": "none",
        elevated: "none",
        glow: "none",
      },
      animation: {
        "fade-in": "fadeIn 0.3s ease-out",
        "slide-up": "slideUp 0.3s ease-out",
        "slide-in": "slideIn 0.25s ease-out",
        "pulse-soft": "pulseSoft 2s ease-in-out infinite",
        "progress": "progressBar 1.5s ease-in-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        slideIn: {
          "0%": { opacity: "0", transform: "translateX(-8px)" },
          "100%": { opacity: "1", transform: "translateX(0)" },
        },
        pulseSoft: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.6" },
        },
        progressBar: {
          "0%": { width: "0%" },
          "100%": { width: "100%" },
        },
      },
    },
  },
  plugins: [],
};
