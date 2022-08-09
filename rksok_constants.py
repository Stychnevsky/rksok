from enum import Enum
from http.client import OK

class RksokRequestCommands(str, Enum):
    GET = 'ОТДОВАЙ'
    POST = 'ЗОПИШИ'
    DELETE = 'УДОЛИ'

class RksokSecurityRequestCommands(str, Enum):
    CHECK = 'АМОЖНА?'

class RksokResponseStatuses(str, Enum):
    OK ='НОРМАЛДЫКС'
    NOT_FOUND = 'НИНАШОЛ'
    INVALID_SECURITY_CHECK = 'НИЛЬЗЯ'
    INCORRECT_REQUEST = 'НИПОНЯЛ'

class RksokSecurityResponseStatuses(str, Enum):
    ALLOWED = 'МОЖНА'
    REJECTED = 'НИЛЬЗЯ'