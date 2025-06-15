from dataclasses import dataclass
from datetime import datetime
import gc
import os


@dataclass
class ModelSettings:
    """ Model settings """
    model_name: str
    model_description: str


MODEL_LIST = dict(
    llama3=ModelSettings(
        model_name="Llama 3.1",
        model_description="Llama 3.1 8B 4bitQ Instruct"
    ),
    qwen3=ModelSettings(
        model_name="Qwen 3",
        model_description="Qwen 3 14B 4bitQ IT"
    ),
)
MODEL_LIST['default'] = MODEL_LIST['qwen3']

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../test/static")
WEBPACK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../test/webpack")


class Session:
    """ Session Manager """
    __sessions: dict[str, 'Session'] = {}
    _initialized = False

    def __new__(cls, model_id: str = None, session_id: str = None):
        """ Create a new session or return an existing one """
        if session_id and session_id in cls.__sessions:
            return cls.__sessions[session_id]
        else:
            return super().__new__(cls)

    def __init__(self, model_id: str = None, session_id: str = None):
        """ Create a new session for the specified model """
        if not self._initialized:
            self._initialized = True

            if model_id is None:
                raise ValueError("Model ID must be specified")
            self.model_id = model_id
            self.session_id = f"{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            print("INFO:     Session", self.session_id, "is CREATED for model", model_id)
            self.__sessions[self.session_id] = self
            print("INFO:     Current sessions:", list(self.__sessions))
            self._model = None

    @property
    def model(self):
        """ Get the model instance for this session """
        if self._model is None:
            self._model = self.load_model(self.model_id)
        return self._model

    @classmethod
    def load_model(cls, model_name: str):
        """ Load a model by its name """
        if model_name not in MODEL_LIST:
            raise ValueError(f"Model '{model_name}' is not supported.")
        exec(f"from .models import {model_name}", globals())
        return globals()[model_name].Model()

    @classmethod
    def close(cls, session_id: str):
        """ Close the session """
        if session_id in cls.__sessions:
            print("INFO:     Session", session_id, "is DELETED for model", cls.__sessions[session_id].model_id)
            import sys
            if sys.getrefcount(cls.__sessions[session_id]._model) <= 3:
                cls.__sessions[session_id]._model.clean_up()
                cls.__sessions[session_id]._model = None  # Clear the model reference
            del cls.__sessions[session_id]
            print("INFO:     Current sessions:", list(cls.__sessions))
            cls.clean_up()
        else:
            raise ValueError(f"Session {session_id} not found")

    @classmethod
    def clean_up(cls):
        gc.collect()
