from services.mail import MailService
from services import dao
from services import common
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

mail = MailService()

KEY_EMAIL = 'email'
KEY_TEMPLATE = 'template'
KEY_SOURCE_IP = 'source_ip'
SUPPORTED_TEMPLATES = ['drink', 'smell']

MAX_EMAILS_PER_IP_PER_MINUTE = 1
MAX_EMAILS_PER_EMAIL_PER_MINUTE = 1

MILLISECONDS_PER_MINUTE = 60 * 1000


def validate_send_email(body, context):
    logger.info('validate_send_email: {}, {}'.format(body, context))

    if KEY_EMAIL not in body \
        or KEY_TEMPLATE not in body \
        or KEY_SOURCE_IP not in context:
        return construct_response_bad_request()

    email = body[KEY_EMAIL]
    template = body[KEY_TEMPLATE]
    source_ip = context[KEY_SOURCE_IP]

    if template not in SUPPORTED_TEMPLATES:
        return construct_response(400, "Given template value is not supported.")

    # check whether from given ip address hasn't been sent email in last 1 minute
    count = dao.get_count_for_ip_address(source_ip, MILLISECONDS_PER_MINUTE)

    if count >= MAX_EMAILS_PER_IP_PER_MINUTE:
        return construct_response(429, "Limit of requests from IP address per minute exceeded.")

    # check whether from given ip address hasn't been sent email in last 1 minute
    count = dao.get_count_for_email(email, MILLISECONDS_PER_MINUTE)

    if count >= MAX_EMAILS_PER_EMAIL_PER_MINUTE:
        return construct_response(429, "Limit of requests for single email per minute exceeded.")

    mail.send_mail(email, template)

    dao.store_ip_address(source_ip)
    dao.store_email(email, template)

    return construct_response(200, "")


def construct_response_bad_request():
    return common.construct_response(400, "Bad request. All required input parameters should be provided.")


def construct_response_server_error():
    return common.construct_response(500, "Something is wrong!")


def construct_response(status_code, message, response_body=None):
    result = {
        'status_code': status_code,
        'body': message if response_body is None else json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    logger.info('constructing response - {}'.format(result))

    return result
