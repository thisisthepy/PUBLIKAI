import { readdir, stat } from 'fs/promises';
import path from 'path';

export interface FileInfo {
	name: string;
	url: string;
	size?: string;
	type?: string;
	year?: string | undefined;
	fullPath?: string;
	isDirectory?: boolean;
}

/**
 * API를 통해 PDF 파일 목록을 가져오기 (빌드된 환경용)
 */
export async function getPdfFilesByYearFromAPI(): Promise<{ [year: string]: FileInfo[] }> {
	try {
		// 현재 환경이 브라우저인지 확인
		if (typeof window !== 'undefined') {
			const response = await fetch('/api/pdf/files');
			if (!response.ok) {
				throw new Error(`API request failed: ${response.status}`);
			}
			return await response.json();
		}
		
		// 서버 사이드에서는 기존 방식 사용
		return await getPdfFilesByYear();
	} catch (error) {
		console.warn('API를 통한 파일 로딩 실패, 기존 방식으로 재시도:', error);
		// API 실패 시 기존 방식으로 폴백
		try {
			return await getPdfFilesByYear();
		} catch (fallbackError) {
			console.error('파일 로딩 완전 실패:', fallbackError);
			return {};
		}
	}
}

/**
 * 파일 크기를 사람이 읽기 쉬운 형태로 변환
 */
function formatFileSize(bytes: number): string {
	if (bytes === 0) {
		return '0 B';
	}
	
	const k = 1024;
	const sizes = ['B', 'KB', 'MB', 'GB'];
	const i = Math.floor(Math.log(bytes) / Math.log(k));
	
	return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/**
 * 파일 확장자에서 타입 추출
 */
function getFileType(fileName: string): string {
	const ext = path.extname(fileName).toLowerCase();
	const typeMap: { [key: string]: string } = {
		'.pdf': 'PDF',
		'.doc': 'DOC',
		'.docx': 'DOCX',
		'.xls': 'XLS',
		'.xlsx': 'XLSX',
		'.ppt': 'PPT',
		'.pptx': 'PPTX',
		'.zip': 'ZIP',
		'.rar': 'RAR',
		'.txt': 'TXT',
		'.hwp': 'HWP'
	};
	
	return typeMap[ext] || ext.slice(1).toUpperCase();
}

/**
 * 파일명이나 경로에서 연도 추출 (2020-2030년 범위)
 */
function extractYear(fileName: string, filePath: string): string | undefined {
	// 1. 먼저 파일 경로에서 연도 폴더 찾기 (예: "/2024년/", "/2025년/")
	const pathYearMatch = filePath.match(/[\\\/](20[2-3]\d)년?[\\\/]/);
	if (pathYearMatch) {
		return pathYearMatch[1] + '년';
	}
	
	// 2. 파일명에서 연도 찾기
	const fileYearMatch = fileName.match(/(20[2-3]\d)/);
	if (fileYearMatch) {
		return fileYearMatch[1] + '년';
	}
	
	return undefined;
}

/**
 * 특정 디렉토리의 모든 파일을 재귀적으로 가져오기
 */
export async function getAllFiles(dirPath: string, baseUrl: string = '/data'): Promise<FileInfo[]> {
	const files: FileInfo[] = [];
	
	try {
		const items = await readdir(dirPath);
		
		for (const item of items) {
			const fullPath = path.join(dirPath, item);
			const stats = await stat(fullPath);
			
			// 상대 경로 계산 (data 폴더 기준)
			const relativePath = path.relative(path.join(process.cwd(), 'data'), fullPath);
			const url = baseUrl + '/' + relativePath.replace(/\\/g, '/');
			
			if (stats.isDirectory()) {
				// 디렉토리인 경우 재귀적으로 탐색
				const subFiles = await getAllFiles(fullPath, baseUrl);
				files.push(...subFiles);
			} else {
				// 파일인 경우 - 확장자 포함한 전체 파일명 사용
				const fileInfo: FileInfo = {
					name: item, // 확장자 포함한 전체 파일명
					url: url,
					size: formatFileSize(stats.size),
					type: getFileType(item),
					year: extractYear(item, fullPath), // 전체 파일명으로 연도 추출
					fullPath: fullPath,
					isDirectory: false
				};
				
				files.push(fileInfo);
			}
		}
	} catch (error) {
		console.error('Error reading directory:', error);
	}
	
	return files;
}

/**
 * PDF 파일만 필터링
 */
export async function getPdfFiles(): Promise<FileInfo[]> {
	const pdfPath = path.join(process.cwd(), 'data', 'pdf');
	const allFiles = await getAllFiles(pdfPath);
	
	// PDF 파일만 필터링하고 연도별, 이름별로 정렬
	return allFiles
		.filter(file => file.type === 'PDF')
		.sort((a, b) => {
			// 연도 역순 (최신 먼저)
			if (a.year && b.year) {
				const yearA = parseInt(a.year);
				const yearB = parseInt(b.year);
				if (yearA !== yearB) {
					return yearB - yearA;
				}
			}
			
			// 이름순
			return a.name.localeCompare(b.name, 'ko');
		});
}

/**
 * 연도별로 그룹화된 파일 목록
 */
export async function getPdfFilesByYear(): Promise<{ [year: string]: FileInfo[] }> {
	const files = await getPdfFiles();
	const grouped: { [year: string]: FileInfo[] } = {};
	
	files.forEach(file => {
		const year = file.year || '기타';
		if (!grouped[year]) {
			grouped[year] = [];
		}
		grouped[year].push(file);
	});
	
	return grouped;
}
