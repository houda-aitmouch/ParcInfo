import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
	plugins: [react()],
	root: __dirname,
	base: "/static/react/",
	build: {
		outDir: path.resolve(__dirname, "../static/react"),
		emptyOutDir: true,
		assetsDir: "assets",
		rollupOptions: {
			output: {
				entryFileNames: "app.js",
				chunkFileNames: "chunks/[name].js",
				assetFileNames: "assets/[name][extname]",
			},
		},
	},
});


