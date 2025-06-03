"""
Core Runtime for managing backend implementations.
"""


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

    def __new__(cls, *args, **kwargs):
        if cls != CoreRuntime:
            backend = cls
        else:
            backend_str = kwargs.get('backend', None)
            if cls.__default_backend is None:
                raise ValueError("None of the backends are registered. Please register at least one backend before using this runtime.")
            backend = cls.__backends.get(backend_str, cls.__backends[cls.__default_backend])
        return backend(*args, **kwargs)
