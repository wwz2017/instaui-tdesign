import { defineConfig } from "vite";
import * as path from "path";
import vue from "@vitejs/plugin-vue";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  server: {
    proxy: {
      "/instaui": {
        target: "http://0.0.0.0:8080",
      },
    },
  },

  define: {
    "process.env": {},
  },

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },

  base: "./",

  build: {
    sourcemap: false,
    lib: {
      entry: path.resolve(__dirname, "src/main.ts"),
      fileName: "instaui-tdesign",
    },
    rollupOptions: {
      external: ["vue", "echarts", "instaui"],
      output: [
        {
          format: "es",
        },
      ],
    },
  },
});
