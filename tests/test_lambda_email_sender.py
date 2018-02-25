import os
import sys
import random


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src import lambda_email_sender

STATUS_CODE = 'status_code'
BODY = 'body'
CODE = 'code'
MESSAGE = 'message'

STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_OK = 200
STATUS_CODE_LIMIT = 429
GENERAL_BAD_REQUEST = "Bad request. All required input parameters should be provided."

BAD_REQUEST_CODE = 'BadRequest'


def generate_random_ip_address():
    return f'{random.randint(0, 256)}' \
           f'.{random.randint(0, 256)}' \
           f'.{random.randint(0, 256)}' \
           f'.{random.randint(0, 256)}'


def validate_result_is_bad_request(result, message=GENERAL_BAD_REQUEST):
    assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST
    assert result[BODY][CODE] == BAD_REQUEST_CODE
    assert result[BODY][MESSAGE] == message


def test_bad_input_missing_source_ip():
    body = {'email': 'friend@email.com', 'template': 'smell'}
    result = lambda_email_sender.lambda_handler(body, None)
    validate_result_is_bad_request(result)


def test_bad_input_missing_template():
    body = {'email': 'friend@email.com', 'source-ip': generate_random_ip_address()}
    result = lambda_email_sender.lambda_handler(body, None)
    validate_result_is_bad_request(result)


def test_bad_input_missing_email():
    body = {'template': 'smell', 'source-ip': generate_random_ip_address()}
    result = lambda_email_sender.lambda_handler(body, None)
    validate_result_is_bad_request(result)


def test_bad_input_unsupported_template():
    body = {'email': 'friend@email.com', 'template': 'not_supported',
            'source-ip': generate_random_ip_address()}
    result = lambda_email_sender.lambda_handler(body, None)
    validate_result_is_bad_request(result, 'Given template value is not supported.')


def test_success():
    body = {'email': 'friend@email.com',
            'template': 'smell', 'source-ip': generate_random_ip_address()}
    result = lambda_email_sender.lambda_handler(body, None)
    assert result[STATUS_CODE] == STATUS_CODE_OK


def test_hitting_limits_email():
    body = {'email': 'different@email.com',
            'template': 'smell', 'source-ip': generate_random_ip_address()}
    result = lambda_email_sender.lambda_handler(body, None)
    assert result[STATUS_CODE] == STATUS_CODE_OK

    body = {'email': 'different@email.com',
            'template': 'smell', 'source-ip': generate_random_ip_address()}
    result = lambda_email_sender.lambda_handler(body, None)
    assert result[STATUS_CODE] == STATUS_CODE_LIMIT
    assert result[BODY][CODE] == 'LimitExceeded'
    assert result[BODY][MESSAGE] == "Limit of requests for single email per minute exceeded."


def test_hitting_limits_ip_address():
    source_ip = generate_random_ip_address()
    body = {'email': 'second@email.com',
            'template': 'smell', 'source-ip': source_ip}
    result = lambda_email_sender.lambda_handler(body, None)
    assert result[STATUS_CODE] == STATUS_CODE_OK

    body = {'email': 'different@gmail.com',
            'template': 'smell', 'source-ip': source_ip}
    result = lambda_email_sender.lambda_handler(body, None)
    assert result[STATUS_CODE] == STATUS_CODE_LIMIT
    assert result[BODY][CODE] == 'LimitExceeded'
    assert result[BODY][MESSAGE] == "Limit of requests from IP address per minute exceeded."
