class WrongRequestFormatError(Exception):
    pass

class WrongProtocolError(WrongRequestFormatError):
    pass

class WrongCommandError(WrongRequestFormatError):
    pass

class TooLongUserNameError(WrongRequestFormatError):
    pass

class UserNameNotDefienedError(WrongRequestFormatError):
    pass

class UserNotFoundError(Exception):
    pass

class ValidationNotPassedError(Exception):
    def __init__(self, validation_server_response: str) -> None:
        self.response = validation_server_response

class WrongResponseFromValidationServerError(Exception):
    pass
