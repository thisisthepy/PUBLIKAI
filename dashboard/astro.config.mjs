import { defineConfig } from 'astro/config';

import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

const DEV_PORT = 8080;
const IS_DEV = process.env.NODE_ENV === 'development';

// https://astro.build/config
export default defineConfig({
	site: IS_DEV ? `http://localhost:${DEV_PORT}` : 'http://localhost:8000',
	base: IS_DEV ? '/' : '/dashboard',
	output: 'static',
	outDir: './static',
	trailingSlash: IS_DEV ? 'ignore' : 'always',

	server: {
		port: DEV_PORT
	},

	integrations: [
		sitemap(),
		tailwind(),
	]
});
