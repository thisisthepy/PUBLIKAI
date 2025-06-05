from dataclasses import dataclass
from datetime import datetime
from copy import deepcopy
from json import dumps

from .embedding import *
from .web_search import *


@dataclass
class FunctionCalling:
    schemas: list[dict]
    implementations: dict


@dataclass
class FunctionSchema(dict):
    name: str
    description: str
    parameters: dict


class FunctionCallResult(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.job_list = []
        self.append(dict(
            role="assistant",
            content=None,
            tool_calls=self.job_list
        ))

    def do(self, name: str, arguments: dict):
        job_id = datetime.now().strftime("call_%Y%m%d%H%M%S")
        result = FUNCTIONS.implementations[name](arguments)
        self.job_list.append(dict(id=job_id, function=dict(
            name=name,
            arguments=arguments
        )))
        self.append(dict(role="tool", tool_call_id=job_id, content=result))
        return "<tool_call>" + dumps([
            dict(id=job_id, function=dict(
                name=name,
                arguments=deepcopy(arguments)
            )),
            dict(role="tool", tool_call_id=job_id, content=f"<cached_result:{job_id}>")
        ]) + "</tool_call>"


FUNCTIONS = FunctionCalling(
    schemas=[
        FunctionSchema(
            name="get_weather",
            description="Get current weather information for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get weather for"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        ),
        FunctionSchema(
            name="calculate",
            description="Perform mathematical calculations",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        )
    ],

    implementations=dict(
        get_weather=lambda location, unit="celsius": f"Weather in {location}: 22°{'C' if unit == 'celsius' else 'F'}, sunny",
        calculate=lambda expression: eval(expression) if expression else "Invalid expression"
    )
)
