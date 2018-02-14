import boto3
import time
import logging

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client_dynamo = boto3.client('dynamodb', region_name='us-east-1')
resource_dynamo = boto3.resource('dynamodb', region_name='us-east-1')

TABLE_NAME_EMAILS = 'intervention_ninja_emails_cache'
TABLE_NAME_IP_ADDRESSES= 'intervention_ninja_ips_cache'


def get_counts(email, source_ip_address):
    logger.info('get_counts for both tables')
    response = client_dynamo.batch_get_item(
        RequestItems={
            TABLE_NAME_EMAILS: {
                'Keys': [
                    {
                        'email':
                            {
                                'S': email
                            }
                    }
                ]
            },
            TABLE_NAME_IP_ADDRESSES: {
                'Keys': [
                    {
                        'ip_address':
                            {
                                'S': source_ip_address
                            }
                    }
                ]
            }

        },
        ReturnConsumedCapacity='NONE'
    )
    logger.info(f'get_counts response: {response}')
    items = response['Responses']
    ip_item = items[TABLE_NAME_IP_ADDRESSES]

    if len(ip_item) == 0:
        ip_item = None

    email_item = items[TABLE_NAME_EMAILS]

    if len(email_item) == 0:
        email_item = None

    return ip_item, email_item


result = get_counts('pkrayzel@gmail.com', '127.0.0.1')

print(result)
