import traceback
from typing import Generator, Tuple, Optional, List, Dict, Union

from .config import ChatHistory
from ..backend import BackendType


class BaseModel:
    """
    Base model class that can be extended by other models. (Singleton pattern)
    """
    __instance = None
    _initialized = False

    model_id = ""
    context_length = 0
    supported_backends: Tuple[BackendType] = tuple([BackendType.DEFAULT])

    def __new__(cls, *args, **kwargs):
        """ Ensure only one instance of the model is created """
        if cls.__instance is None:
            cls.__instance = super(BaseModel, cls).__new__(cls)
        return cls.__instance

    def __init__(self, backend: BackendType = BackendType.DEFAULT):
        if not self._initialized:
            self._initialized = True
            print("INFO:     Model", self.model_id, "is LOADED")

    def __del__(self):
        """ Clean up resources when the model is deleted """
        if hasattr(self, 'runtime'):
            del self.runtime
        self._initialized = False
        print("INFO:     Model", self.model_id, "is UNLOADED")

    def clean_up(self):
        """ Clean up resources for the model """
        self.__class__.__instance = None

    def chat(
        self,
        chat_history: ChatHistory,
        user_prompt: str,
        system_prompt: str = "",
        tools: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.2,
        top_p: float = 0.95,
        top_k: int = 40,
        min_p: float = 0.05,
        typical_p: float = 1.0,
        stream: bool = True,
        max_new_tokens: int = 512,
        repeat_penalty: float = 1.0,
        print_output: bool = False
    ) -> Union[Generator[str], str]:
        """ Process a chat request """
        prompt = chat_history.create_prompt(system_prompt, user_prompt)
        chat_history.append("user", user_prompt)

        if print_output:
            print("PROMPT:")
            for line in prompt:
                print(line)
            print()

        outputs = self.runtime(
            messages=prompt,
            tools=tools,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            min_p=min_p,
            typical_p=typical_p,
            stream=stream,
            max_new_tokens=max_new_tokens,
            repeat_penalty=repeat_penalty
        )

        if print_output:
            print("ANSWER:")

        if stream:
            try:
                for word in outputs:
                    if word:
                        print(word, end="")
                    yield word
            except ValueError:  # Over token limit error
                traceback.print_exc()
                message = "\n\nERROR: Chat is unexpectedly terminated due to token limit. Please shorten your prompt or chat history."
                if print_output:
                    print(message, end="")
                yield message
            finally:
                print()
        else:
            print(outputs)
