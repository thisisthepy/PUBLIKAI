import traceback
from re import finditer, DOTALL
from dataclasses import dataclass
from typing import Generator, Tuple, Optional, List, Dict, Union

from .config import ChatHistory
from ..backend import BackendType
from ..utils import FunctionCalling, FunctionCallResult


@dataclass
class Tags:
    """
    Tags for the model, used for filtering and searching.
    """
    REASONING: str = "<think>"
    REASONING_END: str = "</think>"
    TOOLCALL: str = "<tool_call>"
    TOOLCALL_END: str = "</tool_call>"


class BaseModel:
    """
    Base model class that can be extended by other models. (Singleton pattern)
    """
    __instance = None
    _initialized = False

    model_id = ""
    context_length = 0
    supported_backends: Tuple[BackendType] = tuple([BackendType.DEFAULT])
    supported_tools: FunctionCalling = FunctionCalling.DEFAULT
    special_tags = Tags()

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

    def parse_tool_calling(
        self,
        outputs,
        chat_history: ChatHistory,
        tools: List[Dict[str, str]],
        stream: bool = True
    ) -> Union[Generator[str, None, None], str]:
        """ Parse tool calling from the model's output """
        if len(tools) == 0:
            return outputs

        result_obj = FunctionCallResult()
        result_obj.register_tools(tools, self.supported_tools.implementations)

        if stream:
            started = False
            buffer = ""
            for word in outputs:
                if self.special_tags.TOOLCALL in word:  # Start of a tool call
                    started = True
                    if buffer:
                        buffer = 0
                elif self.special_tags.TOOLCALL_END in word:  # End of a tool call
                    if buffer:
                        result_obj.stage(
                            buffer,
                            (self.special_tags.TOOLCALL, self.special_tags.TOOLCALL_END)
                        )
                        state = result_obj.state
                        if state is not None:
                            yield state
                    buffer = ""
                    started = False
                else:
                    if started:
                        buffer += word
                        state = result_obj.state
                        if state is not None:
                            yield state
                    else:
                        yield word
        else:
            original_outputs = outputs
            outputs = outputs.replace(self.special_tags.TOOLCALL, "").replace(self.special_tags.TOOLCALL_END, "")

            for match in finditer(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", original_outputs, DOTALL):
                json_string = match.group(1)  # Extract the JSON string from the match
                outputs.replace(json_string, "")  # Remove the tool call from the output
                result_obj.stage(
                    json_string,
                    (self.special_tags.TOOLCALL, self.special_tags.TOOLCALL_END)
                )

        # Finalize the tool calls
        print("")
        spinner = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
        stat = 0
        while True:
            final_result = result_obj.finalize(
                chat_history,
                (self.special_tags.TOOLCALL, self.special_tags.TOOLCALL_END)
            )
            if stat % 2 == 0:
                print(f"\r{spinner[(stat//2) % len(spinner)]} Waiting for tool calls to finish...", end="", flush=True)
            if final_result is False:
                stat += 1
                continue
            print("\r[✔] Tool calls are finalized successfully.")

            if stream:
                yield final_result
                break
            else:
                return outputs + final_result

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
        """ Process a chat request

        Args:
            chat_history (ChatHistory): Chat history
            user_prompt (str): User prompt
            system_prompt (str, optional): System prompt. Defaults to "".
            tools (Optional[List[Dict[str, str]]], optional): Tools. Defaults to None. Pass empty list to disable tools.
            temperature (float, optional): Temperature. Defaults to 0.2.
            top_p (float, optional): Top p. Defaults to 0.95.
            top_k (int, optional): Top k. Defaults to 40.
            min_p (float, optional): Min p. Defaults to 0.05.
            typical_p (float, optional): Typical p. Defaults to 1.0.
            stream (bool, optional): Stream. Defaults to True.
            max_new_tokens (int, optional): Max new tokens. Defaults to 512.
            repeat_penalty (float, optional): Repeat penalty. Defaults to 1.0.
            print_output (bool, optional): Print output. Defaults to False.
            **kwargs: Additional arguments
        """
        initial_operation = True
        function_called = True
        while function_called:
            function_called = False

            prompt = chat_history.create_prompt(system_prompt, user_prompt)
            if user_prompt is not None:
                chat_history.append("user", user_prompt)
            else:
                prompt = prompt[:-1]  # Remove the last user prompt if it's None
            user_prompt = None  # Reset user prompt to None after appending

            if print_output and initial_operation:
                print("PROMPT:")
                for line in prompt:
                    print(line)
                print("\nANSWER:")
            initial_operation = False

            tools = tools if tools is not None else self.supported_tools.schemas

            generation_kwargs = dict(
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
            generation_kwargs.update(kwargs)
            outputs = self.parse_tool_calling(
                self.runtime(**generation_kwargs),
                chat_history=chat_history,
                tools=tools,
                stream=stream
            )

            if stream:
                try:
                    for word in outputs:
                        if word:
                            if self.special_tags.TOOLCALL in word and self.special_tags.TOOLCALL_END in word:
                                function_called = True  # flag on
                            if print_output: print(word, end="")
                            yield word
                except ValueError as e:  # Over token limit error
                    traceback.print_exc()
                    if "token" in str(e) and "limit" in str(e):
                        message = "\n\nERROR: Chat is unexpectedly terminated due to token limit. Please shorten your prompt or chat history."
                    else:
                        message = f"\n\nERROR: {type(e)} - Something went wrong while processing the chat. Please try again later.\n{e}"
                    if print_output: print(message, end="")
                    yield message
                finally:
                    print()
            else:
                if self.special_tags.TOOLCALL in outputs and self.special_tags.TOOLCALL_END in outputs:
                    function_called = True  # flag on
                print(outputs)
