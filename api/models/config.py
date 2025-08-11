from datetime import datetime, date, timezone
from typing import Iterable
import time


def clean_text(problematic_text: str) -> str:
    """ Clear non-UTF8 characters (such as emojis) to avoid UnicodeEncodeError """
    try:
        clean = problematic_text.encode('utf-8', 'surrogatepass').decode('utf-8', 'ignore')
        clean.encode('utf-8')
        return clean
    except UnicodeDecodeError:  # Safe fallback for surrogate pairs
        return "".join(char for char in problematic_text if ord(char) < 0xD800 or ord(char) > 0xDFFF)
    except Exception:  # Non-string input handling
        return problematic_text


class ChatHistory(list):
    """ Chat history class """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def append(self, role: str | Iterable[str], content: str | Iterable[str]):
        if isinstance(content, str):
            if isinstance(role, str):
                super().append({'role': role, 'content': clean_text(content)})
            else:
                raise ValueError("Role must be a string when content is a string")
        else:
            if isinstance(role, str):
                role = [role for _ in content]
            for r, c in zip(role, content):
                super().append({'role': r, 'content': clean_text(c)})

    def extend(self, history: Iterable):
        for item in history:
            try:
                self.append(**item)
            except TypeError:
                if (
                    (isinstance(item, dict) and 'role' in item and 'content' in item
                    and isinstance(item['role'], str) and isinstance(item['content'], str))
                    or (isinstance(item, dict) and 'role' in item and 'tool_calls' in item
                        and isinstance(item['role'], str) and isinstance(item['tool_calls'], list))
                ):
                    super().append({k: clean_text(v) for k, v in item.items()})
                else:
                    raise ValueError("Each item must be a dictionary with 'role' and 'content' keys or a Message object. But got: " + str(item))

    def create_prompt(self, system_prompt: str, user_prompt: str = ""):
        return [
            {
                'role': "system",
                'content': f"현재 유저의 지역 시간은: {datetime.now()} {date.today().strftime('%a').upper()} ({time.tzname[0]}). 참고사항으로, 해당 UTC 시간은 {datetime.now(timezone.utc)}입니다. " + system_prompt
            },
            *self,
            {
                'role': "user",
                'content': user_prompt
            }
        ]
