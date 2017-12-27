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
        logger.info("event type: {}, context type: {}"
                    .format(type(event), type(context)))

        data = event

        body = data if KEY_BODY not in data else data[KEY_BODY]
        context_body = data if KEY_CONTEXT not in data else data[KEY_CONTEXT]

        logger.info('body: {}, context_body: {}'.format(body, context_body))

        return common.validate_send_email(body, context_body)
    except Exception as e:
        logger.error('Exception during sending email: %s', e)
        return common.construct_response_server_error()
