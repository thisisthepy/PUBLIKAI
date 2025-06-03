from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import torch

pip install auto-gptq optimum

model_name = "Qwen/Qwen2.5-14B-Instruct"
save_path = "./qwen3-14b-gptq-4bit"

# GPTQ 양자화 설정
quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=False,
)

# 모델 로드
print("모델 로딩 중...")
model = AutoGPTQForCausalLM.from_pretrained(
    model_name,
    quantize_config,
    device_map="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# 양자화 수행 (캘리브레이션 데이터셋 필요)
print("양자화 수행 중...")
# 간단한 캘리브레이션 데이터
calibration_data = [
    "이것은 테스트 문장입니다.",
    "양자화를 위한 샘플 데이터입니다.",
    # 더 많은 샘플 데이터 추가 가능
]

model.quantize(calibration_data)

# 저장
print("양자화된 모델 저장 중...")
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"GPTQ 양자화된 모델이 {save_path}에 저장되었습니다.")





from auto_gptq import AutoGPTQForCausalLM
from transformers import AutoTokenizer

save_path = "./qwen3-14b-gptq-4bit"

# 저장된 GPTQ 모델 로드
model = AutoGPTQForCausalLM.from_quantized(
    save_path,
    device_map="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(save_path, trust_remote_code=True)

print("GPTQ 양자화된 모델 로딩 완료!")

