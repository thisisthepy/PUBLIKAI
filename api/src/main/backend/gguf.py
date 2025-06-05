try:
    from llama_cpp import Llama, CreateChatCompletionStreamResponse

    from typing import List, Dict, Optional, Union, Generator
    import os

    from .core import CoreRuntime


    class GGUFRuntime(CoreRuntime):
        def __init__(self,
            model_id: str,
            context_length: int = 12000,
            cache_dir: Optional[Union[str, os.PathLike[str]]] = None,
            **kwargs
        ):
            self.model_id = model_id
            self.context_length = context_length

            kwargs['repo_id'] = model_id
            kwargs['cache_dir'] = cache_dir
            kwargs['n_ctx'] = context_length
            if 'verbose' not in kwargs:
                kwargs['verbose'] = False

            self.model = Llama.from_pretrained(**kwargs)

        def __call__(
            self,
            messages: List[Dict[str, str]],
            tools: Optional[List[Dict[str, str]]] = None,
            temperature: float = 0.2,
            top_p: float = 0.95,
            top_k: int = 40,
            min_p: float = 0.05,
            typical_p: float = 1.0,
            stream: bool = False,
            max_new_tokens: int = 512,
            repeat_penalty: float = 1.0,
            **kwargs
        ) -> Union[Generator[str, None, None], str]:
            generation_kwargs = dict(
                messages=messages,
                tools=tools,
                max_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                min_p=min_p,
                typical_p=typical_p,
                repeat_penalty=repeat_penalty,
                stream=stream
            )
            generation_kwargs.update(kwargs)
            outputs = self.model.create_chat_completion(**generation_kwargs)

            if stream:
                for token in outputs:
                    delta: dict = token['choices'][0]['delta']
                    token_delta = delta.get('content')
                    if token_delta:
                        yield token_delta
            else:
                return outputs['choices'][0]['text']

    CoreRuntime.register_backend("GGUFRuntime", GGUFRuntime, default=True)
except ImportError:
    print("WARNING: llama_cpp module is not installed. Please install it to use GGUFRuntime.")
