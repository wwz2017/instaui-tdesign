// vite.config.tdesign.ts
import { defineConfig } from "vite";
import * as path from "path";

export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(
        __dirname,
        "node_modules/tdesign-vue-next/es/index.mjs"
      ),
      name: "TDesignVueNext",
      formats: ["es"],
      fileName: () => "tdesign.min.js",
    },
    rollupOptions: {
      external: ["vue"],
      output: {
        assetFileNames: (assetInfo) => {
          if (
            assetInfo.type === "asset" &&
            assetInfo.names?.some((n) => n.endsWith(".css"))
          ) {
            return "tdesign.min.css";
          }
          return "[name][extname]";
        },
      },
    },
    outDir: "dist/tdesign-dist",
  },
});
