import boto3
import logging
import os
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('sns', region_name='us-east-1')


def publish(email, template):
    logger.info('Sending message to SNS topic...')
    topic_arn = os.environ.get('TOPIC_ARN')
    message = {"email": email, "template": template}
    response = client.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

    message_id = response['MessageId']
    logger.info(f'message successfully sent with message id: {message_id}')
