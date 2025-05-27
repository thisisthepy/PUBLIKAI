import traceback
from typing import Iterator

from llama_cpp import  CreateChatCompletionStreamResponse

from .config import ChatHistory


class BaseModel:
    """
    Base model class that can be extended by other models. (Singleton pattern)
    """
    __instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """ Ensure only one instance of the model is created """
        if cls.__instance is None:
            cls.__instance = super(BaseModel, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True

            if not hasattr(self, 'model_id'):
                raise ValueError("Model ID must be set.")

            if not hasattr(self, 'context_length'):
                raise ValueError("Context length must be set.")

            print("INFO:     Model", self.model_id, "is LOADED")

    def __del__(self):
        """ Clean up resources when the model is deleted """
        if hasattr(self, 'model'):
            if hasattr(self.model, 'free'):
                self.model.free()
            del self.model
        self._initialized = False
        print("INFO:     Model", self.model_id, "is UNLOADED")

    def clean_up(self):
        """ Clean up resources for the model """
        self.__class__.__instance = None

    def __call__(
            self, prompt: list, temperature: float, tools: list | None = None, tool_choice: str = "auto"
    ) -> Iterator:
        """ Call the model with the given arguments """
        raise NotImplementedError("Call method must be implemented by subclasses.")

    def chat(
            self, chat_history: ChatHistory, user_prompt: str,
            system_prompt: str, temperature: float = 0.5, print_prompt: bool = True,
            tools: list | None = None, tool_choice: str = "auto"
    ) -> tuple[Iterator, bool]:
        """ Process a chat request """
        prompt = chat_history.create_prompt(system_prompt, user_prompt)
        chat_history.append("user", user_prompt)

        if print_prompt:
            print("PROMPT:")
            for line in prompt:
                print(line)
            print()

        return self(prompt, temperature=temperature, tools=tools, tool_choice=tool_choice), print_prompt

    def stream_tokens(self, *args, **kwargs) -> Iterator[str]:
        """ Stream tokens for the chat response """
        raise NotImplementedError("Token streamer method must be implemented by subclasses.")


def llama_cpp_token_streamer(tokens: Iterator[CreateChatCompletionStreamResponse], print_prompt: bool = True) -> Iterator[str]:
    """ Llama.cpp Token streamer """
    if print_prompt:
        print("ANSWER:")

    try:
        for token in tokens:
            delta: dict = token['choices'][0]['delta']
            token_delta = delta.get('content')
            if token_delta:
                print(token_delta, end="")
            yield token_delta if token_delta else ""
    except ValueError:  # Over token limit error
        traceback.print_exc()
        yield "\n\nERROR: Chat is unexpectedly terminated due to token limit. Please shorten your prompt or chat history."
    finally:
        print()
