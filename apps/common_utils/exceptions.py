from rest_framework.exceptions import (APIException, AuthenticationFailed, ErrorDetail, MethodNotAllowed,
                                       NotAcceptable, NotAuthenticated, NotFound, ParseError, PermissionDenied,
                                       Throttled, UnsupportedMediaType, ValidationError)
from rest_framework.views import exception_handler

exception_codes = {
    ErrorDetail: 1,
    APIException: 1,
    ValidationError: 2,
    ParseError: 3,
    AuthenticationFailed: 4,
    NotAuthenticated: 5,
    PermissionDenied: 6,
    NotFound: 7,
    MethodNotAllowed: 8,
    NotAcceptable: 9,
    UnsupportedMediaType: 10,
    Throttled: 11,
}


def custom_exception_handler(exc, context):
    def _parse_dict_exc(data):
        r = list()
        for key, value in data.items():
            if not isinstance(value, list):
                value = [value]
            new_error_value = []
            for single_error in value:
                error_number = exception_codes.get(exc.__class__, 0)
                new_error_value.append({'text': single_error, 'code_number': error_number})
            error = {'field': key, 'messages': new_error_value}
            r.append(error)
        return r

    response = exception_handler(exc, context)

    if response is not None:
        customized_response = list()
        if isinstance(response.data, dict):
            customized_response = _parse_dict_exc(response.data)
        elif isinstance(response.data, list):
            for d in response.data:
                customized_response += _parse_dict_exc(d)
        response.data = customized_response

    return response
