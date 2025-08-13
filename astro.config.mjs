import { defineConfig } from 'astro/config';

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

const DEV_PORT = 8080;
const IS_DEV = process.env.NODE_ENV === 'development';

// https://astro.build/config
export default defineConfig({
	site: IS_DEV ? `http://localhost:${DEV_PORT}` : 'http://localhost:8000',
	base: IS_DEV ? '/' : '/dashboard',
	output: 'static',
	srcDir: './dashboard',
	trailingSlash: IS_DEV ? 'ignore' : 'always',

	server: {
		port: DEV_PORT
	},
	
	  // 🔽 여기 추가
  vite: {
    resolve: {
      alias: {
        // v1 경로 → v2 분리 패키지로 매핑 (소스 수정 없이 해결)
        'flowbite/dist/datepicker.js': 'flowbite-datepicker',
      },
    },
  },

	integrations: [
		sitemap(),
		tailwind(),
		mdx(),
	]
});
