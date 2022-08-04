from consts import PROTOCOL
from typing import Optional

class RksokResponse:
    def __init__(self, answer: str, body: Optional[str] = None):
        self.answer = answer
        self.body = body

    def raw_response(self) -> str:
        body = '\r\n' + self.body if self.body else ''
        response = f'{self.answer} {PROTOCOL}{body}\r\n\r\n'
        return response
