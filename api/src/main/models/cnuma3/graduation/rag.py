# 파일 경로: src/main/models/graduation_rag/rag.py
import logging
from typing import Dict, List, Optional

from langchain.docstore.document import Document
from .parser import GraduationRequirementParser
from .vector_store import VectorStoreManager

class GraduationRAG:
    def __init__(self, md_files_by_year: Optional[Dict[int, str]] = None, vector_store_path: Optional[str] = None):
        self.parser = GraduationRequirementParser()
        self.vector_store_manager = VectorStoreManager()
        self.retriever = None
        if md_files_by_year:
            self.initialize_from_markdown_files(md_files_by_year)
        elif vector_store_path:
            self.initialize_from_vector_store(vector_store_path)
        else:
            raise ValueError("md_files_by_year 또는 vector_store_path 중 하나는 반드시 제공되어야 합니다.")
    def _format_data_to_documents(self, all_parsed_data: Dict[str, List[Dict]]) -> List[Document]:
        all_docs = []
        for college, rows in all_parsed_data.items():
            for row in rows:
                content = ""
                for key, value in row.items():
                    content += f"{key}: {value}\n"
                doc = Document(page_content=content, metadata=row)
                all_docs.append(doc)
        return all_docs
    def initialize_from_markdown_files(self, md_files_by_year: Dict[int, str]):
        logging.info("여러 마크다운 파일 처리 시작...")
        all_parsed_data = {}
        for year, file_path in md_files_by_year.items():
            logging.info(f"'{file_path}' ({year}년도) 파일 처리 중...")
            parsed_data_for_year = self.parser.parse_from_markdown(file_path, year)
            for college, rows in parsed_data_for_year.items():
                if college not in all_parsed_data:
                    all_parsed_data[college] = []
                all_parsed_data[college].extend(rows)
        logging.info("파싱된 데이터를 문서 형식으로 변환 중...")
        documents = self._format_data_to_documents(all_parsed_data)
        self.vector_store_manager.create_vector_store(documents)
        self.retriever = self.vector_store_manager.get_retriever()
        if self.retriever:
            logging.info("RAG 시스템 초기화 완료.")
        else:
            logging.error("RAG 시스템 초기화 실패: 벡터 저장소가 생성되지 않았습니다.")
    def initialize_from_vector_store(self, vector_store_path: str):
        logging.info("저장된 벡터 저장소로부터 초기화 중...")
        self.vector_store_manager.load_vector_store(vector_store_path)
        self.retriever = self.vector_store_manager.get_retriever()
        logging.info("RAG 시스템 초기화 완료.")
    def save_vector_store(self, path: str):
        self.vector_store_manager.save_vector_store(path)
    def answer_question(self, question: str) -> str:
        if not self.retriever:
            return "시스템이 초기화되지 않았습니다. 입력 파일을 확인 후 다시 시도해주세요."
        logging.info(f"질문 처리 중: {question}")
        relevant_docs = self.retriever.get_relevant_documents(question)
        if not relevant_docs:
            return "관련된 졸업요건 정보를 찾을 수 없습니다."
        answer = f"--- 질문: {question} ---\n\n"
        answer += "--- 답변: 관련 졸업요건 정보 ---\n\n"
        for i, doc in enumerate(relevant_docs, 1):
            answer += f"✅ [검색된 정보 {i}]\n"
            answer += f"{doc.page_content.strip()}\n\n"
        return answer