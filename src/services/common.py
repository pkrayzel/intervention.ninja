from services.mail import MailService
from services.template import TemplateServiceS3
from services import dao
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

mail = MailService()
mail_template_service = TemplateServiceS3('www.intervention.ninja', 'emails/')

KEY_EMAIL = 'email'
KEY_TEMPLATE = 'template'
KEY_SOURCE_IP = 'source-ip'
SUPPORTED_TEMPLATES = ['drink', 'smell']

MAX_EMAILS_PER_IP_PER_MINUTE = 1
MAX_EMAILS_PER_EMAIL_PER_MINUTE = 1

MILLISECONDS_PER_MINUTE = 60 * 1000

MAIL_SUBJECT = 'Intervention Ninja - personal message'
MAIL_SENDER = 'intervention.ninja@gmail.com'


def validate_send_email(body, context):
    logger.info('validate_send_email: {}, {}'.format(body, context))

    if KEY_EMAIL not in body:
        logger.warning('Missing required parameter: {}'.format(KEY_EMAIL))
        return construct_response_bad_request()
    elif KEY_TEMPLATE not in body:
        logger.warning('Missing required parameter: {}'.format(KEY_TEMPLATE))
        return construct_response_bad_request()
    elif KEY_SOURCE_IP not in context:
        logger.warning('Missing required parameter: {}'.format(KEY_SOURCE_IP))
        return construct_response_bad_request()

    email = body[KEY_EMAIL]
    template = body[KEY_TEMPLATE]
    source_ip = context[KEY_SOURCE_IP]

    if template not in SUPPORTED_TEMPLATES:
        logger.warning('Template is not supported: {}. Should be one of: {}'
                       .format(template, SUPPORTED_TEMPLATES))
        return construct_response_bad_request("Given template value is not supported.")

    # check whether from given ip address hasn't been sent email in last 1 minute
    count = dao.get_count_for_ip_address(source_ip, MILLISECONDS_PER_MINUTE)

    if count >= MAX_EMAILS_PER_IP_PER_MINUTE:
        logger.warning('Maximum emails from IP: {} per minute achieved: {}'
                       .format(source_ip, count))
        return construct_response_limit_exceeded("Limit of requests from IP address per minute exceeded.")

    # check whether from given ip address hasn't been sent email in last 1 minute
    count = dao.get_count_for_email(email, MILLISECONDS_PER_MINUTE)

    if count >= MAX_EMAILS_PER_EMAIL_PER_MINUTE:
        logger.warning('Maximum emails {} per minute achieved: {}'
                       .format(email, count))
        return construct_response_limit_exceeded("Limit of requests for single email per minute exceeded.")

    content_html = mail_template_service.render_template('{}.html'.format(template))

    mail.send_mail(MAIL_SUBJECT, MAIL_SENDER, email, content_html)

    dao.store_ip_address(source_ip)
    dao.store_email(email, template)
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
    logger.info('constructing error response - {}'.format(result))
    return result


def _construct_response_success(response_body=None):
    result = {
        'status_code': 200,
        'body': '' if response_body is None else json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
    logger.info('constructing success response - {}'.format(result))
    return result
