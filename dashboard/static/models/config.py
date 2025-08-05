from browser import module_init
print, pyprint = module_init(__name__, "models.config")
########################################################################################################################
from typing import Iterable


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

    def raw_extend(self, history: Iterable):
        """ Append raw items without cleaning them """
        super().extend(history)
