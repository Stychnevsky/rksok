from exceptions import (UserNotFoundError, WrongProtocolError, TooLongUserNameError, WrongRequestFormatError,
WrongCommandError, UserNameNotDefienedError)
from database_client import DatabaseClient as DbClient
from rksok_response import RksokResponse
from security_validator import SecurityValidator
from loguru import logger
from config import PROTOCOL, USER_NAME_MAX_LEN
from typing import Tuple
from rksok_constants import RksokRequestCommands as commands
from rksok_constants import RksokResponseStatuses as statuses


class RksokServer:
    def __init__(self, data: str):
        self.data = data
    
    @staticmethod
    def check_protocol(first_line: str) -> None:
        if not first_line.endswith(' ' + PROTOCOL):
            raise WrongProtocolError

    @staticmethod
    def check_rksok_command(command: str) -> None:
        for rksok_command in commands:
            if command == rksok_command:
                return
        raise WrongProtocolError

    def parse_request(self) -> Tuple[str, str, str]:
        splited_data = self.data[:-4].split('\r\n') # TODO изменить -4 на END
        first_line = splited_data[0]
        self.check_protocol(first_line)
        request_body = self.data[len(first_line) + 2:-4]
        
        first_line = first_line.rstrip(PROTOCOL) # TODO: опасное использование PROTOCOL
        command = first_line.split()[0]
        self.check_rksok_command(command)
        user = first_line.lstrip(command).strip()

        if not user:
            logger.warning('Server cant find user name in request!')
            raise UserNameNotDefienedError

        if len(user) > USER_NAME_MAX_LEN:
            logger.warning(f'Too long user name length! Max is {}')
            raise TooLongUserNameError
        return command, user, request_body

    def validate_request(self) -> None:
        request_to_check = f'АМОЖНА? {PROTOCOL}\r\n{self.data}' # TODO обернуть АМОЖНА
        self.validation_ok, self.validation_response = SecurityValidator(request_to_check).validate_request()

    async def process_request(self) -> str:
        try:
            command, user, request_body = self.parse_request()
        except WrongRequestFormatError:
            logger.warning('Wrong request!')
            return RksokResponse(status=statuses.INCORRECT_REQUEST).generate_response()

        self.validate_request()
        if not self.validation_ok:
            return self.validation_response
        
        db_client = DbClient()
        try:
            if command == commands.GET:
                    user_date = await db_client.get_user_data(user)

            elif command == commands.POST:
                user_date = None
                await db_client.add_user(user, request_body)

            elif command ==commands.DELETE:
                user_date = None
                await db_client.delete_user(user)

            response = RksokResponse(status=statuses.OK, body=user_date).generate_response()
            logger.debug(f'Response from server: {response}')
            return response

        except UserNotFoundError:
            logger.warning(f'User {user} not found in database')
            return RksokResponse(status=statuses.NOT_FOUND).generate_response()
