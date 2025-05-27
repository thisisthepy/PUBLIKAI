from dataclasses import dataclass

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
