import json
from services.dao import *
from services import common

KEY_EMAIL = 'email'
KEY_TEMPLATE = 'template'
KEY_SOURCE_IP = 'source-ip'


def lambda_handler(event, context):
    try:
        logging.info("lambda_handler event: {} context {}".format(json.dumps(event, indent=2), context))
        body = json.loads(event['body'])
        context_body = json.loads(event['context'])

        if KEY_EMAIL not in body \
                or KEY_TEMPLATE not in body \
                or KEY_SOURCE_IP not in context:
            return common.construct_response_bad_request()

        return common.validate_send_email(body, context_body)
    except Exception as e:
        logging.error('Exception during sending email', e)
        return common.construct_response_server_error()
