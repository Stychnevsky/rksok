import socket
from exceptions import WrongResponseFromValidationServerError
from consts import ENCODING
from loguru import logger

VALIDATION_SERVER = 'vragi-vezde.to.digital'
VALIDATION_PORT = 51624

class RequestValidator:
    def __init__(self, data):
        self.data = data
        self._conn = None
    
    def parse_response(self): # придумать как лучше обработать
        data = self.response

        if data[:6] == "НИЛЬЗЯ":
            logger.warning('REJECTED answer from validation server recieved')
            response = False, data
            return response
        
        elif data[:5] == 'МОЖНА':
            logger.debug('OK answer from validation server recieved')
            return True, None

        raise WrongResponseFromValidationServerError

    def validate_request(self):
        if not self._conn:
            self._conn = socket.create_connection((VALIDATION_SERVER, VALIDATION_PORT))
        self._conn.sendall(self.data.encode(ENCODING))
        logger.debug('Send request to validation server')
        response = b""

        while True:
            data = self._conn.recv(1024)
            logger.debug(f'Response from validation server recieved:{data.decode(ENCODING)}')
            if not data: break
            response += data
        self.response = response.decode(ENCODING)
        return self.parse_response()
