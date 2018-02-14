import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def construct_response_bad_request(
        message="Bad request. All required input parameters should be provided."):
    return _construct_response_error(400, message, "BadRequest")


def construct_response_limit_exceeded(message):
    return _construct_response_error(429, message, "LimitExceeded")


def construct_response_server_error():
    return _construct_response_error(500, "Something is wrong!", "GeneralError")


def _construct_response_error(status_code, message, code):
    result = {
        'status_code': status_code,
        'body': {'code': code, 'message': message},
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    logger.info(f'constructing error response - {result}')
    return result


def construct_response_success(response_body=None):
    result = {
        'status_code': 200,
        'body': '' if response_body is None else json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    logger.info(f'constructing success response - {result}')
    return result
