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
    supported_tools: List[Dict[str, str]] = None

    def __new__(cls, *args, **kwargs):
        """ Ensure only one instance of the model is created """
        if cls.__instance is None:
            cls.__instance = super(BaseModel, cls).__new__(cls)
        return cls.__instance

    def __init__(self, backend: BackendType | None = None):
        if not self._initialized:
            self._initialized = True
            self.runtime = self._get_runtime(backend)
            print("INFO:     Model", self.model_id, "is LOADED")

    def _get_runtime(self, backend: BackendType | None = None):
        if backend not in self.supported_backends:
            raise ValueError(f"Unsupported backend: {backend}. Supported backends are: {self.supported_backends}")

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
        print_output: bool = False,
        **kwargs
    ) -> Union[Generator[str, None, None], str]:
        """ Process a chat request """
        prompt = chat_history.create_prompt(system_prompt, user_prompt)
        if user_prompt is not None:
            chat_history.append("user", user_prompt)
        else:
            prompt = prompt[:-1]  # Remove the last user prompt if it's None

        if print_output:
            print("PROMPT:")
            for line in prompt:
                print(line)
            print()

        generation_kwargs = dict(
            messages=prompt,
            tools=tools if tools is not None else self.supported_tools,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            min_p=min_p,
            typical_p=typical_p,
            stream=stream,
            max_new_tokens=max_new_tokens,
            repeat_penalty=repeat_penalty
        )
        generation_kwargs.update(kwargs)
        outputs = self.runtime(**generation_kwargs)

        if print_output:
            print("ANSWER:")

        if stream:
            try:
                for word in outputs:
                    if word:
                        if print_output:
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
