from json import dumps, loads, JSONDecodeError
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar
from copy import deepcopy

from concurrent.futures import ThreadPoolExecutor
import threading

from . import weather
from . import calculator
from . import embedding
from . import web_search
from . import calendar
from . import currency


@dataclass
class FunctionCalling:
    schemas: list[dict]
    implementations: dict

    DISABLED: ClassVar['FunctionCalling'] = None
    DEFAULT: ClassVar['FunctionCalling'] = None


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

        self.schemas: list[dict] = FunctionCalling.DEFAULT.schemas
        self.implementations: dict = FunctionCalling.DEFAULT.implementations

        self.__queue_mutex = threading.Lock()
        self.__thread_pool = ThreadPoolExecutor()
        self.__completed_jobs = 0
        self.__message_queue: list[str] = []

    def register_tools(self, schemas: list[dict], implementations: dict):
        """ Register tools with their schemas and implementations """
        if self.job_list:
            raise RuntimeError("Cannot register tools after job list has been created.")
        else:
            self.schemas = schemas
            # Keep only the implementations that are in the schemas
            names = {schema['name'] for schema in schemas}
            self.implementations = {
                name: impl for name, impl in implementations.items() if name in names
            }

    @property
    def state(self):
        with self.__queue_mutex:
            if not self.__message_queue:
                return None
            else:
                # Return the current state of the message queue
                queue = self.__message_queue
                self.__message_queue = []
                return "\n" + "\n".join(queue)

    def finalize(
        self,
        history_list: list,
        tag: tuple[str, str] = ("<tool_call>", "</tool_call>")
    ) -> str | False:
        # Check if there are any pending tool calls
        with self.__queue_mutex:
            if len(self.job_list) != self.__completed_jobs:
                return False
            else:  # If no pending tool calls, finalize the result
                # Update the history with the current state
                history_list.extend(deepcopy(self))

                # Dump client-side tool call history
                state = self.state
                if state is None:
                    state = ""
                for data in self:
                    if 'tool_call_id' in data:
                        data['content'] = f"<cached_result:{data['tool_call_id']}>"
                result = state + "\n" + tag[0] + dumps(self) + tag[1]

                # Clear the job list and message queue
                self.job_list = []
                self.__completed_jobs = 0
                self.__message_queue = []
                return result

    def stage(self, calling: str, tag: tuple[str, str] = ("<tool_call>", "</tool_call>")):
        with self.__queue_mutex:
            job_id = datetime.now().strftime("call_%Y%m%d%H%M%S")
            try:
                params = loads(calling)
            except JSONDecodeError:
                pass  # TODO: Handle invalid JSON format if needed (in the future)
            name, arguments = params.get("name"), params.get("arguments")

            self.job_list.append(dict(id=job_id, function=dict(
                name=name,
                arguments=arguments
            )))
            self.__message_queue.append(tag[0] + dumps(dict(call=dict(id=job_id, function=dict(
                name=name, arguments=deepcopy(arguments)
            )))) + tag[1])

            self.__thread_pool.submit(self.do, job_id, name, arguments, tag)

    def do(
        self,
        job_id: str,
        name: str,
        arguments: dict,
        tag: tuple[str, str] = ("<tool_call>", "</tool_call>")
    ):
        # Execute the function
        try:
            if name not in self.implementations:
                raise ValueError(f"Function '{name}' is not registered.")
            result = self.implementations[name](**arguments)
        except Exception as e:
            result = str(e)

        # History and result handling
        with self.__queue_mutex:
            # Server side
            self.append(dict(role="tool", tool_call_id=job_id, content=result))

            # Client side
            self.__message_queue.append(tag[0] + dumps(dict(result=dict(id=job_id, function=dict(
                content=f"<cached_result:{job_id}>"
            )))) + tag[1])  # for immediate response

            # Increment the completed job count
            self.__completed_jobs += 1


FunctionCalling.DISABLED = FunctionCalling(schemas=[], implementations={})
FunctionCalling.DEFAULT = FunctionCalling(
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
            name="get_weather_forecast",
            description="Get weather forecast for a location",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get forecast for"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-16, supported by Open-Meteo API)",
                        "minimum": 1,
                        "maximum": 16
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
            name="get_calendar_events",
            description="Get calendar events (holidays and special observances) for a specific date",
            parameters={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format"
                    },
                    "country": {
                        "type": "string",
                        "description": "ISO country code (US, KR, JP, GB, etc.)",
                        "default": "US"
                    }
                },
                "required": ["date"]
            }
        ),
        FunctionSchema(
            name="get_upcoming_holidays",
            description="Get upcoming holidays within the specified number of days",
            parameters={
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "ISO country code (US, KR, JP, GB, etc.)",
                        "default": "US"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to look ahead (default: 30)",
                        "default": 30,
                        "minimum": 1,
                        "maximum": 365
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_exchange_rate",
            description="Get exchange rate and convert currency amount",
            parameters={
                "type": "object",
                "properties": {
                    "from_currency": {
                        "type": "string",
                        "description": "Source currency code (e.g., USD, EUR, KRW)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Target currency code (e.g., USD, EUR, KRW)"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount to convert (default: 1.0)",
                        "default": 1.0,
                        "minimum": 0.01
                    }
                },
                "required": ["from_currency", "to_currency"]
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
        get_weather=weather.get_weather,
        get_weather_forecast=weather.get_weather_forecast,
        get_calendar_events=calendar.get_calendar_events,
        get_upcoming_holidays=calendar.get_upcoming_holidays,
        get_exchange_rate=currency.get_exchange_rate,
        calculate=calculator.calculate
    )
)
