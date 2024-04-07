import react from '@vitejs/plugin-react';
import * as path from 'path';
import { defineConfig } from 'vite';
import svgr from 'vite-plugin-svgr';
// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react(), svgr()],
	server: {
		proxy: {
			'/api/': {
				target: 'https://amazing-digital-misis.ru:8000/',
				changeOrigin: true,
			},
		},
		port: 3000,
	},
	resolve: {
		alias: {
			'@media': path.resolve('./src/media'),
			'@pages': path.resolve('./src/pages'),
			'@models': path.resolve('./src/models'),
			'@static': path.resolve('./src/static'),
			'@components': path.resolve('./src/components'),
		},
	},
	css: {
		modules: {
			scopeBehaviour: 'local',
			localsConvention: 'camelCase',
			generateScopedName: '[local]__[hash:base64:2]',
		},
	},
});
