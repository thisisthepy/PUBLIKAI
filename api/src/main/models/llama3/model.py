from typing import Iterator

from llama_cpp import Llama, CreateChatCompletionStreamResponse

from ..base import ChatHistory, BaseModel, llama_cpp_token_streamer


# Set model id
model_id = "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF"
context_length = 128000  # Set context length to 128000 tokens


# Prompt setting
system_prompt = "" \
                + "Your name is `Llama 3.1` developed by Meta AI. " \
                + "You are a helpful, smart, kind, and efficient AI Assistant. " \
                + "Your knowledge is based on data available up to December 2023. " \
                + "You always fulfill the user's requests to the best of your ability. " \
                + "You are not aware of any events or developments that occurred after that date unless explicitly provided by the user. " \
                + "Do not fabricate information about events beyond your knowledge cutoff. If uncertain, state that clearly. " \
                + "Detect the user's input language and always respond in the same language. " \
                + "Do not switch languages unless explicitly instructed. " \
                + "Maintain a consistent, polite, and contextually appropriate tone for each language."
print("INFO:     Use default system prompt -", system_prompt)


class Llama3Model(BaseModel):
    """
    Llama 3.1 8B 4bitQ Instruct model implementation.
    This class extends BaseModel and provides methods for chatting and token streaming.
    """

    def __init__(self):
        if not self._initialized:
            # Set model id
            self.model_id = model_id
            self.context_length = context_length
            self._token_streamer = llama_cpp_token_streamer

            # Load model
            self.model = Llama.from_pretrained(
                repo_id=model_id,
                filename="*Q4_K_M.gguf",  # 4bit quantized model
                n_ctx=context_length,
                verbose=False
            )

            super().__init__()

    def __call__(self, prompt: list, temperature: float) -> Iterator[CreateChatCompletionStreamResponse]:
        return self.model.create_chat_completion(
            messages=prompt,
            temperature=temperature,
            stream=True
        )

    def chat(
            self, chat_history: ChatHistory, user_prompt: str,
            system_prompt: str = system_prompt, temperature: float = 0.5, print_prompt: bool = True):
        return super().chat(
            chat_history=chat_history, user_prompt=user_prompt,
            system_prompt=system_prompt, temperature=temperature, print_prompt=print_prompt
        )

    def stream_tokens(self, *args, **kwargs) -> Iterator[str]:
        """
        Stream tokens for the chat response.
        This method uses the llama_cpp_token_streamer to yield tokens from the model.
        """
        return self._token_streamer(*args, **kwargs)
