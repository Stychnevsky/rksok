from optparse import Option
import socket
from exceptions import ValidationNotPassedError, WrongResponseFromValidationServerError
from config import ENCODING, VALIDATION_SERVER, VALIDATION_PORT
from loguru import logger
from typing import Optional, Tuple
from rksok_constants import RksokSecurityResponseStatuses as response_statuses
 
class SecurityValidator:
    def __init__(self):
        self._conn = None
    
    def send_validation_request(self, request_data: str) -> str:
        if not self._conn:
            self._conn = socket.create_connection((VALIDATION_SERVER, VALIDATION_PORT))

        self._conn.sendall(request_data.encode(ENCODING))
        logger.debug('Send request to validation server')
        response = b""

        while True:
            response_data = self._conn.recv(1024)
            logger.debug(f'Response from validation server recieved:{response_data.decode(ENCODING)}')
            if not response_data: break
            response += response_data
        return response.decode(ENCODING)

    @staticmethod
    def parse_response(response: str) -> Optional[bool]: # придумать как лучше обработать
        if response.startswith(response_statuses.REJECTED):
            logger.warning('REJECTED answer from validation server recieved')
            raise ValidationNotPassedError(response)
        
        elif response.startswith(response_statuses.ALLOWED):
            logger.debug('OK answer from validation server recieved')
            return True

        raise WrongResponseFromValidationServerError

    def validate_request(self, data: str) -> Tuple[bool, str]:
        response = self.send_validation_request(data)
        return self.parse_response(response)
