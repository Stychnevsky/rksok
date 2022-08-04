from exceptions import (UserNotFoundError, WrongProtocolError, TooLongUserNameError, WrongRequestFormatError,
WrongCommandError, UserNameNotDefienedError)
from database_client import DatabaseClient as DbClient
from rksok_response import RksokResponse
from request_validator import RequestValidator
from loguru import logger
from consts import PROTOCOL


class RksokServer:
    def __init__(self, data):
        self.data = data
    
    @staticmethod
    def check_protocol(first_line):
        if not (first_line[-9:] == 'РКСОК/1.0' and first_line[-10]==' '):
            raise WrongProtocolError

    @staticmethod
    def check_rksok_command(command):
        if command not in ('ОТДОВАЙ', 'ОТДОВАЙ', 'УДОЛИ' , 'ЗОПИШИ'):
            raise WrongProtocolError

    def parse_request(self):
        splited_data = self.data[:-4].split('\r\n')
        first_line = splited_data[0]
        self.check_protocol(first_line)
        request_body = self.data[len(first_line) + 2:-4] # TODO: сделать const REQUEST_ENDLINE
        
        first_line = first_line.rstrip("РКСОК/1.0") # TODO: небезопасно что 1.1 тоже подойдет тут!! и что пробела не будет!
        command = first_line.split()[0]
        self.check_rksok_command(command)
        user = first_line.lstrip(command).strip()

        if not user:
            logger.warning('Server cant find user name in request!')
            raise UserNameNotDefienedError

        if len(user) > 30:
            logger.warning('Too long user name length! Max is 30')
            raise TooLongUserNameError
        return command, user, request_body

    def validate_request(self):
        
        request_to_check = f'АМОЖНА? {PROTOCOL}\r\n{self.data}' 
        self.validation_ok, self.validation_response = RequestValidator(request_to_check).validate_request()
        logger.debug('Result of validation')

    async def process_request(self):
        try:
            command, user, request_body = self.parse_request() # TODO: лучше это сделать атрибутами класса?
        except WrongRequestFormatError:
            logger.warning('Wrong request!')
            return RksokResponse(answer='НИПОНЯЛ').raw_response() # TODO: лучше raw_response делать в классе выше

        self.validate_request()
        if not self.validation_ok:
            return self.validation_response
        
        db_client = DbClient()
        try:
            if command == 'ОТДОВАЙ':
                    user_date = await db_client.get_user_data(user)

            elif command == 'ЗОПИШИ':
                user_date = None
                await db_client.add_user(user, request_body)

            elif command =='УДОЛИ':
                user_date = None
                await db_client.delete_user(user)

            response = RksokResponse(answer='НОРМАЛДЫКС', body=user_date).raw_response()
            logger.debug(f'Response from server: {response}')
            return response

        except UserNotFoundError:
            logger.warning(f'User {user} not found in database')
            return RksokResponse(answer='НИНАШОЛ').raw_response()
