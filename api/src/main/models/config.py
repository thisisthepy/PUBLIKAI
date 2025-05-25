from typing import Iterable
from datetime import datetime


class ChatHistory(list):
    """ Chat history class """

    def append(self, role: str | Iterable[str], content: str | Iterable[str]):
        if isinstance(content, str):
            if isinstance(role, str):
                super().append({'role': role, 'content': content})
            else:
                raise ValueError("Role must be a string when content is a string")
        else:
            if isinstance(role, str):
                role = [role for _ in content]
            for r, c in zip(role, content):
                super().append({'role': r, 'content': c})

    def extend(self, history: Iterable):
        for item in history:
            try:
                self.append(**item)
            except TypeError:
                self.append(**item.dict())

    def create_prompt(self, system_prompt: str, user_prompt: str = ""):
        return [
            {
                'role': "system",
                'content': f"Current time is {datetime.now()}. " + system_prompt
            },
            *self,
            {
                'role': "user",
                'content': user_prompt
            }
        ]
