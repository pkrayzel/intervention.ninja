import json
import logging
from services.dao import *
from services import common

KEY_BODY = 'body'
KEY_CONTEXT = 'context'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        logger.info("intervention_ninja - lambda_handler event: {} context {}"
                    .format(json.dumps(event, indent=2), context))

        body = event if KEY_BODY not in event else event[KEY_BODY]
        context_body = event if KEY_CONTEXT not in event else event[KEY_CONTEXT]

        logger.info('body: {}, context_body: {}'.format(body, context_body))

        return common.validate_send_email(body, context_body)
    except Exception as e:
        logger.error('Exception during sending email: %s', e)
        return common.construct_response_server_error()
