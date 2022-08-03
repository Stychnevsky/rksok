from consts import PROTOCOL

class RksokResponse:
    def __init__(self, answer, body=None):
        self.answer = answer
        self.body = body

    def raw_response(self):
        body = '\r\n' + self.body if self.body else ''
        response = f'{self.answer} {PROTOCOL}{body}\r\n\r\n'
        return response
