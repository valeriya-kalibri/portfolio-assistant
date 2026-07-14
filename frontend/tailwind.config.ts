import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        gold: {
          DEFAULT: "#D4AF37",
          dark: "#A67C00",
          light: "#F5D06F",
        },
        ink: "#060606",
      },
    },
  },
  plugins: [],
};

export default config;
