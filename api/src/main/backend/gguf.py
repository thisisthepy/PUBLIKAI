from typing import List, Tuple, Dict, Optional, Union, Generator
import sys
import os
import gc

from .core import CoreRuntime


try:
    from llama_cpp import Llama, CreateChatCompletionStreamResponse


    class GGUFRuntime(CoreRuntime):
        def __init__(self,
            model_id: str,
            context_length: int = 12000,
            cache_dir: Optional[Union[str, os.PathLike[str]]] = None,
            gpu_layer_attempts: Tuple[int] = (-1, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0),
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

            if sys.platform == "win32":  # settings against Windows CUDA error
                gpu_layer_attempts = (0, )

            last_error = None

            for n_layers in gpu_layer_attempts:
                try:
                    try:
                        import torch
                        if torch.cuda.is_available():
                            torch.cuda.empty_cache()
                    except:
                        pass
                    gc.collect()

                    kwargs_copy = kwargs.copy()
                    kwargs_copy['n_gpu_layers'] = n_layers

                    self.model = Llama.from_pretrained(**kwargs_copy)

                    print(f"INFO:     Model {model_id} loaded with {n_layers} GPU layers.")

                    # Display GPU memory usage (if available)
                    try:
                        from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown
                        if n_layers > 0:
                            handle = nvmlDeviceGetHandleByIndex(0)
                            meminfo = nvmlDeviceGetMemoryInfo(handle)
                            memory_allocated = meminfo.used / 1024**3
                            total_memory = meminfo.total / 1024**3
                            nvmlShutdown()
                            print(f"INFO:     GPU memory usage: {memory_allocated:.2f}GB / {total_memory:.2f}GB")
                    except:
                        pass
                    return
                except Exception as e:
                    print(f"ERROR:    Memory allocation error occurred while loading {model_id} model with {n_layers} layers: {e}")

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
    GGUFRuntime = CoreRuntime.DUMMY_BACKEND
