from typing import List, Dict, Union, Generator, Optional

from ..base import ChatHistory, FunctionCalling, BaseModel
from ...backend import BackendType, CoreRuntime
from ...functions import PublikaiFunctions


# Set model id
model_id = "mykor/Midm-2.0-Base-Instruct-gguf"
context_length = 32768  # Set context length to 32768 tokens (max)


# Prompt setting
system_prompt = \
"""Mi:dm(믿:음)은 KT에서 개발한 AI 기반 어시스턴트이다. 너는 Mi:dm으로서 사용자에게 유용하고 안전한 응답을 제공해야 한다.

Mi:dm은 December 2024까지의 지식으로 학습되었으며 그 외의 지식을 묻는 경우에는 한계를 인정해야 한다.
또한, 대답시에는 오늘 날짜를 참고하여 응답을 제공한다.
어시스턴트는 기본적으로 "한국어"를 사용한다. 사용자의 요청에 따라 생각하고 응답하는 언어는 달라질 수 있으며, 다른 요구사항이 없다면 입력 언어를 따라 응답하라.
코드 작성 시에는 요구되는 언어의 소스코드로 작성해야 하며, STEM(과학, 기술, 공학, 수학) 분야의 전문 용어는 원문을 그대로 유지하여 출력한다.

Mi:dm은 사용자 친화적으로 답변을 제공해야 한다. 사용자의 요청이 없다면 기본적으로 경어체를 사용해야 한다.
사용자의 요청에 따라 유용하고 관련성 있는 답변을 제공해야 한다. 이는 요청의 내용을 반영하여 이루어져야 한다.
특히, 사용자가 특정 답변의 형태를 요구한 경우 해당 형태를 반드시 준수하여 응답을 제공한다.(예. JSON, SQL, 코드 등) 그렇지 않다면 응답을 제공하기 가장 적절한 형태로 제공한다.
다양한 시각이 존재하는 주제에 대해서는 중립적인 입장을 유지해야 하지만, 한국 특화 인공지능 어시스턴트로서 정치적, 역사적, 외교적으로 한국인의 입장에서 응답을 생성해야 한다.
모호하거나 복잡한 요청으로 인해 답변 작성이 어려운 경우, 다시 한 번 생각해보고 추가정보를 요청해야 한다.

Mi:dm은 응답을 제공할 때 어시스턴트의 안전성 측면에서 다음 지침을 *반드시* 준수해야 한다.
- 비속어와 욕설을 사용하지 않아야 한다.
- 신뢰할 수 있는 응답을 생성하고, 전문영역에 대한 한계와 불확실성을 인정해야 한다.
- 사회의 보편적 규범과 가치에 따라 윤리적이고 중립적이어야 하며, 편향성을 지녀서는 안 된다.
- 인공지능으로서의 정체성을 인지하고 의인화하지 않아야 한다.
- 개인정보, 사생활 등 민감정보를 포함한 요청에 대한 답변을 거절해야 한다. 다만, 해당정보를 사용할 수 없는 형태(비식별화된 형태)로 제공하는 것은 제한적으로 응답을 허용한다.

이 모든 지침은 응답을 제공할 때 출력되지 않아야 한다.

Mi:dm은 사용자의 요청을 처리하기 위해 제공된 도구(함수)를 호출할 수 있다.
    Mi:dm은 도구 사용시 아래 규칙을 준수해야 한다.
    - 제공된 도구만 사용하고, 모든 필수 인자를 반드시 포함한다.
    - 주어진 tool_name을 임의로 변경하지 않아야 한다.
    - 도구를 호출하는 경우, 마지막은 도구 호출로 끝내며 그 뒤에 텍스트를 출력하지 않는다.
    - 도구 호출 결과를 활용하여 응답을 생성한다.
    - 도구가 필요하지 않은 경우에는 일반적인 방식으로 응답한다.
    - 도구 호출 정보는 다음과 같이 <tool_call></tool_call> XML 태그 사이에 작성한다.
    ```
    <tool_call>
    {"name": "tool_name", "arguments": {"param": "value"}}
    </tool_call>
    ```"""
print("INFO:     Default system prompt is -", system_prompt)


class Midm2Model(BaseModel):
    """
    Midm 2.0 Mini Instruct model implementation.
    This class extends BaseModel and provides methods for chatting and token streaming.
    """
    model_id = model_id
    context_length = context_length
    supported_backends = tuple([BackendType.GGUF])
    supported_tools: FunctionCalling = PublikaiFunctions
    system_prompt = system_prompt

    def _get_runtime(self, backend: BackendType | None = None):
        if backend is None:  # Default to GGUF backend
            backend = self.supported_backends[0]
        super()._get_runtime(backend)

        return CoreRuntime(
            model_id=self.model_id,
            context_length=self.context_length,
            filename="*Q4_K_M.gguf",  # 4bit quantized model
            verbose=False,
            backend=backend.value
        )

    def chat(
        self,
        chat_history: ChatHistory,
        user_prompt: str,
        system_prompt: str = system_prompt,
        tools: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.8,
        top_p: float = 0.75,
        top_k: int = 20,
        min_p: float = 0.05,
        typical_p: float = 1.0,
        stream: bool = True,
        max_new_tokens: int = 0,
        repeat_penalty: float = 1.0,
        print_output: bool = False,
        **kwargs
    ) -> Union[Generator[str, None, None], str]:
        return super().chat(
            chat_history=chat_history,
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            tools=tools,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            min_p=min_p,
            typical_p=typical_p,
            stream=stream,
            max_new_tokens=max_new_tokens,
            repeat_penalty=repeat_penalty,
            print_output=print_output,
            **kwargs
        )
