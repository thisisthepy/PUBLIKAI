from enum import Enum
from .core import CoreRuntime
from .bin import BinRuntime
from .gguf import GGUFRuntime


class BackendType(Enum):
    BIN = BinRuntime
    GGUF = GGUFRuntime
