import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,css}'],
  theme: {
    extend: {},
  },
  plugins: [],
  future: {
    respectDefaultRingColorOpacity: true,
    hoverOnlyWhenSupported: true,
  },
};

export default config;
