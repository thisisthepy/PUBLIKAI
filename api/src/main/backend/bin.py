from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import os

from .core import CoreRuntime


SAVE_PATH = os.path.join(os.path.dirname(__file__), ".cache")
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)


class BinRuntime(CoreRuntime):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.tokenizer =








quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

model_name =

save_path = "./qwen3-14b-4bit"  # 저장할 경로

# 원본 모델 로드 및 양자화
print("원본 모델 로딩 및 양자화 중...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quantization_config,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype=torch.float16,
)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# 양자화된 모델과 토크나이저 저장
print("양자화된 모델 저장 중...")
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"양자화된 모델이 {save_path}에 저장되었습니다.")







print("저장된 양자화 모델 로딩 중...")
model = AutoModelForCausalLM.from_pretrained(
    save_path,
    device_map="auto",
    trust_remote_code=True,
    torch_dtype=torch.float16,
)

tokenizer = AutoTokenizer.from_pretrained(save_path, trust_remote_code=True)

print("양자화된 모델 로딩 완료!")

# 추론 함수
def generate_response(prompt, max_length=512):
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=max_length,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# 사용 예시
prompt = "안녕하세요. 인공지능에 대해 설명해주세요."
response = generate_response(prompt)
print(response)

