from services import dao_batch
from services import notification
import logging
import json
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from datetime import datetime
import time


KEY_BODY = 'body'
KEY_CONTEXT = 'context'

KEY_EMAIL = 'email'
KEY_TEMPLATE = 'template'
KEY_SOURCE_IP = 'source-ip'
SUPPORTED_TEMPLATES = ['drink', 'smell']

MAX_EMAILS_PER_IP_PER_MINUTE = 1
MAX_EMAILS_PER_EMAIL_PER_MINUTE = 1

MILLISECONDS_PER_MINUTE = 60 * 1000

logger = logging.getLogger()
logger.setLevel(logging.INFO)

patch_all()


def lambda_handler(event, context):
    try:
        logger.info('intervention_ninja - lambda_handler')

        body = event if KEY_BODY not in event else event[KEY_BODY]
        context_body = event if KEY_CONTEXT not in event else event[KEY_CONTEXT]

        return validate_send_email(body, context_body)
    except Exception as e:
        logger.error('Exception during sending email: %s', e)
        return construct_response_server_error()


@xray_recorder.capture('validate_send_email')
def validate_send_email(body, context):
    xray_recorder.begin_subsegment('argument_validation')

    if KEY_EMAIL not in body:
        logger.warning(f'Missing required parameter: {KEY_EMAIL}')
        return construct_response_bad_request()
    elif KEY_TEMPLATE not in body:
        logger.warning(f'Missing required parameter: {KEY_TEMPLATE}')
        return construct_response_bad_request()
    elif KEY_SOURCE_IP not in context:
        logger.warning(f'Missing required parameter: {KEY_SOURCE_IP}')
        return construct_response_bad_request()

    email = body[KEY_EMAIL]
    template = body[KEY_TEMPLATE]
    source_ip = context[KEY_SOURCE_IP]

    if template not in SUPPORTED_TEMPLATES:
        logger.warning(f'Template is not supported: {template}. Should be one of: {SUPPORTED_TEMPLATES}')
        return construct_response_bad_request("Given template value is not supported.")

    logger.info(f'Validation succeeded! '
                f'Email: {email}, template: {template}, source_ip: {source_ip}')

    xray_recorder.end_subsegment()
    xray_recorder.begin_subsegment('ip_address_limit_check')

    timestamp_minute_before = int(time.mktime(datetime.now().timetuple())) * 1000 - MILLISECONDS_PER_MINUTE

    logger.info(f'Comparing timestamp: {timestamp_minute_before} with current values in DynamoDB to check limits.')

    # check whether from given ip address hasn't been sent email in last 1 minute
    ip_item, email_item = dao_batch.get_items(email, source_ip)

    if ip_item is not None and ip_item['timestamp'] >= timestamp_minute_before:
        logger.warning(f'Maximum emails from IP: {source_ip} per minute achieved.')
        return construct_response_limit_exceeded("Limit of requests from IP address per minute exceeded.")

    xray_recorder.end_subsegment()
    xray_recorder.begin_subsegment('email_limit_check')

    # check whether from given ip address hasn't been sent email in last 1 minute
    if email_item is not None and email_item['timestamp'] >= timestamp_minute_before:
        logger.warning(f'Maximum emails {email} per minute achieved.')
        return construct_response_limit_exceeded("Limit of requests for single email per minute exceeded.")

    logger.info('Both limits checked. All good to continue.')

    xray_recorder.end_subsegment()
    xray_recorder.begin_subsegment('store_values')

    # store sender info + receiver email to dynamo (limit purposes)
    dao_batch.store_items(email, template, source_ip)
    logger.info('Successfully stored new limits to DynamoDB.')

    xray_recorder.end_subsegment()

    xray_recorder.begin_subsegment('sns_publish')
    # publish to sns topic
    notification.publish(email, template)
    logger.info('Successfully published message to SNS.')
    xray_recorder.end_subsegment()

    # return success response
    return _construct_response_success()


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


def _construct_response_success(response_body=None):
    result = {
        'status_code': 200,
        'body': '' if response_body is None else json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    logger.info(f'constructing success response - {result}')
    return result

