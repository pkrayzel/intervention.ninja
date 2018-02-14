from services.mail import MailService
from services.template import TemplateServiceS3
import logging
import json
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)

mail = MailService()
mail_template_service = TemplateServiceS3('www.intervention.ninja', 'emails/')

MAIL_SUBJECT = 'Intervention Ninja - personal message'
MAIL_SENDER = 'intervention.ninja@gmail.com'

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

        xray_recorder.begin_subsegment(f'render_template_{i+1}')

        content_html = mail_template_service.render_template(f'{template}.html')
        logger.info(f'Template {template} successfully rendered')

        xray_recorder.end_subsegment()
        xray_recorder.begin_subsegment(f'send_email_{i+1}')

        mail.send_mail(MAIL_SUBJECT, MAIL_SENDER, email, content_html)

        logger.info(f'Email with template {template} has been successfully sent to address: {email}')
        xray_recorder.end_subsegment()

    xray_recorder.end_segment()
