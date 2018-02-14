from services import dao, notification
from model.arguments import Arguments
import constants
from utils import time, response

import logging

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)

patch_all()


def lambda_handler(event, context):
    xray_recorder.begin_segment('intervention.ninja.sns.publisher')
    try:
        logger.info('Intervention Ninja - starting lambda function...')

        body = event if constants.KEY_BODY not in event else event[constants.KEY_BODY]
        context_body = event if constants.KEY_CONTEXT not in event else event[constants.KEY_CONTEXT]

        validation_result, error_response, arguments \
            = validate_input_arguments(body, context_body)

        if not validation_result:
            return error_response

        within_limit, error_response = check_limits(arguments)

        if not within_limit:
            return error_response

        update_limits(arguments)
        send_email(arguments)
        xray_recorder.end_segment()
        return response.construct_response_success()
    except Exception as e:
        logger.error('Exception during sending email: %s', e)
        xray_recorder.end_segment()
        return response.construct_response_server_error()


@xray_recorder.capture('argument_validation')
def validate_input_arguments(body, context):
    """
    :param body: body of the message, should contain email and template parameter
    :param context: should contain source ip address
    :return: tuple of validation success (True/False), error result (None if success is True,
    otherwise contains constructed error response), arguments class if success is True, otherwise None
    """
    logger.info('Validating input arguments...')

    if constants.KEY_EMAIL not in body \
            or constants.KEY_TEMPLATE not in body \
            or constants.KEY_SOURCE_IP not in context:
        logger.warning('One of the required paramaters is missing')
        return False, response.construct_response_bad_request(), None

    email = body[constants.KEY_EMAIL]
    template = body[constants.KEY_TEMPLATE]
    source_ip = context[constants.KEY_SOURCE_IP]

    if template not in constants.SUPPORTED_TEMPLATES:
        logger.warning(f'Template is not supported: {template}. Should be one of: {SUPPORTED_TEMPLATES}')
        return False, response.construct_response_bad_request("Given template value is not supported."), None

    logger.info(f'Validation succeeded! '
                f'Email: {email}, template: {template}, source_ip: {source_ip}')
    return True, None, Arguments(email, template, source_ip)


@xray_recorder.capture('check_limits')
def check_limits(arguments):
    """
    :param arguments: arguments class with input fields from the original event
    :return: tuple of limit_exceeded (True / False), error_response (when limit exceeded is True, otherwise None)
    """
    logger.info('Checking for exceeding limits of the service.')
    timestamp = time.get_timestamp_minute_ago()

    logger.info(f'Comparing timestamp: {timestamp} with current values in DynamoDB to check limits.')

    # check whether from given ip address hasn't been sent email in last 1 minute
    ip_item, email_item = dao.get_items(arguments.email, arguments.source_ip_address)

    if ip_item is not None and ip_item['timestamp'] >= timestamp:
        logger.warning(f'Maximum emails from IP: {arguments.source_ip_address} per minute achieved.')
        return False, response.construct_response_limit_exceeded(
            "Limit of requests from IP address per minute exceeded.")

    # check whether from given ip address hasn't been sent email in last 1 minute
    if email_item is not None and email_item['timestamp'] >= timestamp:
        logger.warning(f'Maximum emails {arguments.email} per minute achieved.')
        return False, response.construct_response_limit_exceeded(
            "Limit of requests for single email per minute exceeded.")

    logger.info('Both limits checked. All good to continue.')
    return True, None


@xray_recorder.capture('store_values_for_limits')
def update_limits(arguments):
    logger.info('Updating DynamoDB to store values for new limits')
    dao.store_items(arguments.email, arguments.template, arguments.source_ip_address)
    logger.info('Successfully stored new limits to DynamoDB.')


@xray_recorder.capture('sns_publish')
def send_email(arguments):
    # publish to sns topic
    notification.publish(arguments.email, arguments.template)
    logger.info('Successfully published message to SNS.')
