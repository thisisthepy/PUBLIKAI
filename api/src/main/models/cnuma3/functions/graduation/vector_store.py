import logging
from typing import List

import torch
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

class VectorStoreManager:
    def __init__(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model_kwargs = {'device': device}
        logging.info(f"임베딩 모델을 '{device}' 장치에서 실행합니다.")
        self.embedding = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask", model_kwargs=model_kwargs)
        self.vector_store = None
    def create_vector_store(self, documents: List[Document]):
        if not documents:
            logging.error("처리할 문서가 없습니다. 입력 파일의 경로, 이름, 내용을 확인해주세요. 벡터 저장소 생성을 중단합니다.")
            return
        logging.info(f"FAISS 벡터 저장소 생성을 시작합니다... (총 {len(documents)}개 문서)")
        self.vector_store = FAISS.from_documents(documents, self.embedding)
        logging.info("FAISS 벡터 저장소 생성이 완료되었습니다.")
    def save_vector_store(self, path: str):
        if self.vector_store:
            logging.info(f"벡터 저장소를 '{path}' 경로에 저장합니다...")
            self.vector_store.save_local(path)
            logging.info("저장 완료.")
        else:
            logging.error("저장할 벡터 저장소가 없습니다.")
    def load_vector_store(self, path: str):
        logging.info(f"'{path}' 경로에서 벡터 저장소를 로드합니다...")
        try:
            self.vector_store = FAISS.load_local(path, self.embedding, allow_dangerous_deserialization=True)
            logging.info("로드 완료.")
        except Exception as e:
            logging.error(f"벡터 저장소 로드 실패: {e}")
    def get_retriever(self):
        if self.vector_store:
            return self.vector_store.as_retriever()
        logging.error("retriever를 가져오기 전에 벡터 저장소를 생성하거나 로드해야 합니다.")
        return None