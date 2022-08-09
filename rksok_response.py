from config import PROTOCOL, REQUEST_END
from typing import Optional

class RksokResponse:
    def __init__(self, status: str, body: Optional[str] = None):
        self.status = status
        self.body = body

    def generate_response(self) -> str:
        body = '\r\n' + self.body if self.body else ''
        response = f'{self.status} {PROTOCOL}{body}{REQUEST_END}'
        return response
