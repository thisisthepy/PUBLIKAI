"""
Core Runtime for managing backend implementations.
"""
from typing import Optional, List, Dict, Union, Generator
import os


class CoreRuntime:
    __backends = {}
    __default_backend = None

    @classmethod
    def register_backend(cls, backend_name: str, backend_class: type, default: bool = False):
        """
        Register a backend class with a specific name.

        Args:
            backend_name (str): The name of the backend.
            backend_class (type): The class implementing the backend.
            default (bool): Whether this backend should be set as the default.
        """
        cls.__backends[backend_name] = backend_class
        print(f"INFO:     Backend '{backend_name}' is registered successfully.")
        if cls.__default_backend is None or default:
            cls.__default_backend = backend_name

    @classmethod
    def set_default_backend(cls, backend_name: str):
        """
        Set the default backend to be used.
        """
        if backend_name in cls.__backends:
            cls.__default_backend = backend_name
        else:
            raise ValueError(f"Backend '{backend_name}' is not registered.")

    def __new__(cls,
        model_id: str,
        context_length: int = 12000,
        cache_dir: Optional[Union[str, os.PathLike[str]]] = None,
        **kwargs
    ):
        if cls != CoreRuntime:
            backend = cls
        else:
            backend_str = kwargs.get('backend', None)
            if cls.__default_backend is None:
                raise ValueError("None of the backends are registered. Please register at least one backend before using this runtime.")
            backend = cls.__backends.get(backend_str, cls.__backends[cls.__default_backend])
        return super().__new__(backend)

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
        repeat_penalty: float = 1.0
    ) -> Union[Generator[str, None, None], str]:
        raise NotImplementedError("The generate method must be implemented by subclasses.")
