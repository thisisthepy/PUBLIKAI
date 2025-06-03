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

