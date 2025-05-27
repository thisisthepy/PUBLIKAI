from llama_cpp import Llama
import torch
import torch.nn as nn

class HybridReasoningClassifier:
    def __init__(self, llama_model_path):
        # llama-cpp로 임베딩
        self.llm = Llama(
            model_path=llama_model_path,
            embedding=True,
            n_ctx=4096
        )

        # PyTorch 분류기
        embedding_dim = 4096  # Qwen3 hidden size
        self.classifier = nn.Sequential(
            nn.Linear(embedding_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(512, 10)  # 10 classes
        )

        self.optimizer = torch.optim.Adam(self.classifier.parameters())
        self.criterion = nn.CrossEntropyLoss()

    def get_reasoning_embedding(self, question):
        reasoning_prompt = f"/think {question}"
        embedding = self.llm.embed(reasoning_prompt)
        return torch.tensor(embedding, dtype=torch.float32)

    def train_step(self, questions, labels):
        embeddings = []
        for q in questions:
            emb = self.get_reasoning_embedding(q)
            embeddings.append(emb)

        X = torch.stack(embeddings)
        y = torch.tensor(labels, dtype=torch.long)

        # Forward pass
        logits = self.classifier(X)
        loss = self.criterion(logits, y)

        # Backward pass
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def predict(self, question):
        embedding = self.get_reasoning_embedding(question)
        with torch.no_grad():
            logits = self.classifier(embedding.unsqueeze(0))
            probabilities = torch.softmax(logits, dim=1)

        return logits, probabilities

# 이 방법이 가장 실용적
hybrid_classifier = HybridReasoningClassifier("qwen3-14b-q4_0.gguf")





from transformers import AutoModel, AutoTokenizer
import torch.nn as nn

# 기본 모델 로드 (HF 방식)
model = AutoModel.from_pretrained("Qwen/Qwen3-14B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-14B")

# 커스텀 헤드 추가
class CustomHead(nn.Module):
    def __init__(self, hidden_size=4096, num_classes=10):
        super().__init__()
        self.base_model = model
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 512),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(512, num_classes)
        )

    def forward(self, input_ids, attention_mask=None):
        outputs = self.base_model(input_ids, attention_mask=attention_mask)
        pooled = outputs.last_hidden_state.mean(dim=1)  # 평균 풀링
        return self.classifier(pooled)

custom_model = CustomHead()

