from enum import Enum
from .core import CoreRuntime
try:
    from .bin import BinRuntime
except Exception as _ignored:
    pass
try:
    from .gguf import GGUFRuntime
except Exception as _ignored:
    pass


class BackendType(Enum):
    DEFAULT = None
    BIN = "BinRuntime"
    GGUF = "GGUFRuntime"
