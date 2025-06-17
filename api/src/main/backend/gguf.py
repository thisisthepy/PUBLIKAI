try:
    from llama_cpp import Llama, CreateChatCompletionStreamResponse

    from typing import List, Tuple, Dict, Optional, Union, Generator
    import torch
    import os
    import gc

    from .core import CoreRuntime


    class GGUFRuntime(CoreRuntime):
        def __init__(self,
            model_id: str,
            context_length: int = 12000,
            cache_dir: Optional[Union[str, os.PathLike[str]]] = None,
            gpu_layer_attempts: Tuple[int] = (-1, 30, 25, 20, 15, 10, 5, 0),
            **kwargs
        ):
            self.model_id = model_id
            self.context_length = context_length

            kwargs['repo_id'] = model_id
            kwargs['cache_dir'] = cache_dir
            kwargs['n_ctx'] = context_length
            if 'verbose' not in kwargs:
                kwargs['verbose'] = False

            if 'n_gpu_layers' in kwargs:
                start_layers = kwargs['n_gpu_layers']
                # start from the n_gpu_layers specified
                gpu_layer_attempts = [l for l in gpu_layer_attempts if l <= start_layers]

            last_error = None

            for n_layers in gpu_layer_attempts:
                try:
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                    gc.collect()

                    kwargs_copy = kwargs.copy()
                    kwargs_copy['n_gpu_layers'] = n_layers

                    self.model = Llama.from_pretrained(**kwargs)

                    print(f"INFO:     Model {model_id} loaded with {n_layers} GPU layers.")

                    # Display GPU memory usage (if available)
                    if torch.cuda.is_available() and n_layers > 0:
                        memory_allocated = torch.cuda.memory_allocated() / 1024**3
                        memory_reserved = torch.cuda.memory_reserved() / 1024**3
                        print(f"INFO:     GPU memory usage: {memory_allocated:.2f}GB (reserved: {memory_reserved:.2f}GB)")

                except Exception as e:
                    error_msg = str(e).lower()
                    last_error = e

                    # Check if it's a CUDA memory error
                    if 'cuda' in error_msg and ('memory' in error_msg or 'out of memory' in error_msg):
                        print(f"ERROR:    Failed due to insufficient VRAM ({n_layers} layers of {model_id})")
                        continue
                    elif 'failed to allocate' in error_msg or 'allocation' in error_msg:
                        print(f"ERROR:    Memory allocation failed ({n_layers} layers of {model_id})")
                        continue
                    else:
                        # If it's a different type of error, don't retry and raise immediately
                        print(f"ERROR:    Unexpected error occurred while loading {model_id} model with {n_layers} layers: {e}")
                        raise e

            # If all attempts failed
            raise RuntimeError(f"ERROR:    Failed to load {model_id} model with all GPU layer configurations. Last error: {last_error}")

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
