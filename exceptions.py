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
    pass

class WrongResponseFromValidationServerError(Exception):
    pass
