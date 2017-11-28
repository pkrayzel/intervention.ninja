import os
import sys
from src.services import common
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

STATUS_CODE = 'status_code'
BODY = 'body'

STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_OK = 200
STATUS_CODE_LIMIT = 429
GENERAL_BAD_REQUEST = "Bad request. All required input parameters should be provided."


def test_bad_input():
    body = {'email': 'friend@email.com', 'template': 'smell'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST
    assert result[BODY] == GENERAL_BAD_REQUEST

    body = {'email': 'friend@email.com', 'source_ip': '127.0.0.1'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST
    assert result[BODY] == GENERAL_BAD_REQUEST

    body = {'template': 'smell', 'source_ip': '127.0.0.1'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST
    assert result[BODY] == GENERAL_BAD_REQUEST

    body = {'email': 'friend@email.com', 'template': 'not_supported',
            'source_ip': '127.0.0.1'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST
    assert result[BODY] == 'Given template value is not supported.'


def test_ok_and_hitting_limits():
    body = {'email': 'friend@email.com',
            'template': 'smell', 'source_ip': '127.0.0.1'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_OK

    body = {'email': 'friend@email.com',
            'template': 'smell', 'source_ip': '127.0.0.2'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_LIMIT
    assert result[BODY] == "Limit of requests for single email per minute exceeded."

    body = {'email': 'second@email.com',
            'template': 'smell', 'source_ip': '1.1.1.1'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_OK

    body = {'email': 'different@gmail.com',
            'template': 'smell', 'source_ip': '1.1.1.1'}
    result = common.validate_send_email(body, body)
    assert result[STATUS_CODE] == STATUS_CODE_LIMIT
    assert result[BODY] == "Limit of requests from IP address per minute exceeded."
