try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextIteratorStreamer
    import torch

    from typing import List, Dict, Optional, Union, Generator
    import threading
    import os

    from .core import CoreRuntime


    class BinRuntime(CoreRuntime):
        __cache_dir = os.path.join(os.path.dirname(__file__), ".cache")

        def __init__(self,
            model_id: str,
            context_length: int = 12000,
            cache_dir: Optional[Union[str, os.PathLike[str]]] = None,
            device_map: str = "auto",
            quantization_config: BitsAndBytesConfig = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            ),
            **kwargs
        ):
            self.model_id = model_id
            self.device_map = device_map
            self.context_length = context_length
            self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
            save_path = os.path.join(self.__cache_dir, model_id)

            kwargs['device_map'] = device_map
            kwargs['cache_dir'] = cache_dir
            kwargs['trust_remote_code'] = True
            if 'torch_dtype' not in kwargs:
                kwargs['torch_dtype'] = torch.float16

            if not os.path.isdir(save_path):
                os.makedirs(save_path)
                kwargs['quantization_config'] = quantization_config

                self.model = AutoModelForCausalLM.from_pretrained(model_id, **kwargs)
                self.model.save_pretrained(save_path)
            else:
                self.model = AutoModelForCausalLM.from_pretrained(save_path, **kwargs)

        @torch.no_grad()
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
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tools=tools,
                add_generation_prompt=True,
                tokenize=False
            )
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.model.device)
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True) if stream else None
            generation_kwargs = dict(
                input_ids=inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature if temperature > 0 else None,
                top_p=top_p,
                top_k=top_k,
                min_p=min_p,
                typical_p=typical_p,
                repetition_penalty=repeat_penalty,
                streamer=streamer,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            generation_kwargs.update(kwargs)

            if stream:
                thread = threading.Thread(target=self.model.generate, kwargs=generation_kwargs)
                thread.start()

                try:
                    for new_text in streamer:
                        yield new_text
                finally:
                    thread.join()
            else:
                outputs = self.model.generate(**generation_kwargs)
                return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    CoreRuntime.register_backend("BinRuntime", BinRuntime)
except ImportError:
    print("WARNING: transformers module is not installed. Please install it to use GGUFRuntime.")
