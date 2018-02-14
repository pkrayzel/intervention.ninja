import boto3
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = boto3.client('ses')


def send_email(email, template):
    logger.info(f'sending a templated email through SES to: {email}')

    ses_template = f'intervention-ninja-{template}'
    logger.info(f'SES template name to use: {ses_template}')

    response = client.send_templated_email(
        Source='no-reply@intervention.ninja',
        Destination={
            'ToAddresses': [
                email,
            ]
        },
        Template=ses_template,
        TemplateData="{}"
    )
    logger.info(f'SES response: {response}')
