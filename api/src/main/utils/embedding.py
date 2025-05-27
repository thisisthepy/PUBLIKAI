def rag_search(full_document, query):

    # 2. RAG 처리 (Function 내부에서)
    # - 문서를 청크로 나누기
    chunks = split_document(full_document)

    # - 임베딩 생성
    embeddings = create_embeddings(chunks)

    # - 쿼리와 유사한 청크 찾기
    relevant_chunks = find_similar_chunks(query, embeddings)

    # 3. 컨텍스트 길이에 맞게 반환
    return combine_chunks(relevant_chunks, max_tokens=1000)



from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.llama_cpp import LlamaCPP

# 1. 모델 로드
llm = LlamaCPP(
    model_path="./models/llama-2-7b-chat.q4_0.bin",
    temperature=0.1,
    max_new_tokens=256,
)

# 2. 문서 로드 & 인덱싱 (한 줄!)
documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)

# 3. 검색 엔진 생성
query_engine = index.as_query_engine(llm=llm)

# 4. 질문하기
response = query_engine.query("학사 규정에서 졸업 요건은?")
print(response)

