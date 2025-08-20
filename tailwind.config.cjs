/* eslint-disable global-require */
/** @type {import('tailwindcss').Config} */
module.exports = {
	content: [
		'./dashboard/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}',
		'./node_modules/flowbite/**/*.js',
	],

	darkMode: 'class',

	theme: {
		extend: {
			colors: {
				primary: {
					50: '#eff6ff',
					100: '#dbeafe',
					200: '#bfdbfe',
					300: '#93c5fd',
					400: '#60a5fa',
					500: '#3b82f6',
					600: '#2563eb',
					700: '#1d4ed8',
					800: '#1e40af',
					900: '#1e3a8a',
				},
			},
			fontFamily: {
				sans: [
					'Inter',
					'ui-sans-serif',
					'system-ui',
					'-apple-system',
					'system-ui',
					'Segoe UI',
					'Roboto',
					'Helvetica Neue',
					'Arial',
					'Noto Sans',
					'sans-serif',
					'Apple Color Emoji',
					'Segoe UI Emoji',
					'Segoe UI Symbol',
					'Noto Color Emoji',
				],
				body: [
					'Inter',
					'ui-sans-serif',
					'system-ui',
					'-apple-system',
					'system-ui',
					'Segoe UI',
					'Roboto',
					'Helvetica Neue',
					'Arial',
					'Noto Sans',
					'sans-serif',
					'Apple Color Emoji',
					'Segoe UI Emoji',
					'Segoe UI Symbol',
					'Noto Color Emoji',
				],
				mono: [
					'ui-monospace',
					'SFMono-Regular',
					'Menlo',
					'Monaco',
					'Consolas',
					'Liberation Mono',
					'Courier New',
					'monospace',
				],
			},
			transitionProperty: {
				width: 'width',
			},
			textDecoration: ['active'],
			minWidth: {
				kanban: '28rem',
			},
			typography: (theme) => ({
				DEFAULT: {
					css: {
						code: {
							backgroundColor: '#f7f5f3',
							color: '#57534e',
							borderRadius: theme('borderRadius.lg'),
							padding: theme('spacing.1.5') + ' ' + theme('spacing.3'),
							fontWeight: '600',
							fontSize: '0.875em',
							border: '1px solid #e7e5e4',
							boxShadow: '0 1px 3px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.8)',
							letterSpacing: '0.025em',
						},
						'code::before': {
							content: '""',
						},
						'code::after': {
							content: '""',
						},
						pre: {
							backgroundColor: '#292524',
							color: '#fafaf9',
							borderRadius: theme('borderRadius.xl'),
							border: '1px solid #44403c',
							boxShadow: '0 4px 16px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
							backdropFilter: 'blur(8px)',
						},
						'pre code': {
							backgroundColor: 'transparent',
							color: 'inherit',
							border: 'none',
							padding: '0',
							boxShadow: 'none',
							fontWeight: '400',
						},
					},
				},
				invert: {
					css: {
						code: {
							backgroundColor: '#3c3c3c',
							color: '#e7e5e4',
							border: '1px solid #525252',
							boxShadow: '0 1px 3px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
						},
						pre: {
							backgroundColor: '#1c1917',
							color: '#fafaf9',
							border: '1px solid #292524',
							boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05)',
						},
					},
				},
			}),
		},
	},

	safelist: [
		// In Markdown (README…)
		'justify-evenly',
		'overflow-hidden',
		'rounded-md',

		// From the Hugo Dashboard
		'w-64',
		'w-1/2',
		'rounded-l-lg',
		'rounded-r-lg',
		'bg-gray-200',
		'grid-cols-4',
		'grid-cols-7',
		'h-6',
		'leading-6',
		'h-9',
		'leading-9',
		'shadow-lg',
		'bg-opacity-50',
		'dark:bg-opacity-80',

		// For Astro one
		'grid',
	],

	plugins: [
		//
		require('flowbite/plugin'),
		require('flowbite-typography'),
		require('@tailwindcss/typography'),
		require('tailwind-scrollbar')({ nocompatible: true }),
	],
};
