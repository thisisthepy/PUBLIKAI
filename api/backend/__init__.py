from enum import Enum

from .core import CoreRuntime
from .bin import BinRuntime
from .gguf import GGUFRuntime


class BackendType(Enum):
    DEFAULT = None
    BIN = "BinRuntime"
    GGUF = "GGUFRuntime"
