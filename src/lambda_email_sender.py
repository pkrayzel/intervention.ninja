from services import mail
import logging
import json
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)

patch_all()


def lambda_handler(event, context):
    xray_recorder.begin_segment('intervention.ninja.email.sender')

    logger.info(f'lambda handler event: {event}')
    records = event['Records']

    logger.info(f'Number of emails to send out: {len(records)}')

    for i, item in enumerate(records):
        logger.info(f'Preparing to send email number {i+1}...')

        message = json.loads(item['Sns']['Message'])
        template = message['template']
        email = message['email']

        mail.send_email(email, template)

        logger.info(f'Email with template {template} has been successfully sent to address: {email}')

    xray_recorder.end_segment()
