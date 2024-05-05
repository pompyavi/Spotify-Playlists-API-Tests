from enum import Enum
from collections import namedtuple

# Define a named tuple to hold additional data
StatusCodeData = namedtuple('StatusCodeData', ['code', 'message'])


class StatusCode(Enum):
    SUCCESS = StatusCodeData(code=200, message='')
    BAD_REQUEST = StatusCodeData(code=400, message='Missing required field: name')
    UNAUTHORIZED = StatusCodeData(code=401, message='Invalid access token')
    FORBIDDEN = StatusCodeData(code=403, message='Forbidden')
    NOT_FOUND = StatusCodeData(code=404, message='Not Found')
    INTERNAL_SERVER_ERROR = StatusCodeData(code=500, message='Internal Server Error')
    SERVICE_UNAVAILABLE = StatusCodeData(code=503, message='Service Unavailable')
