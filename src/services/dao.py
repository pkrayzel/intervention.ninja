import boto3
import logging
from datetime import datetime
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client_dynamo = boto3.client('dynamodb')

TABLE_NAME_EMAILS = 'intervention_ninja_emails_cache'
TABLE_NAME_IP_ADDRESSES = 'intervention_ninja_ips_cache'


def store_items(email, template, source_ip):
    logger.info(f'Writing batch items into dynamodb: '
                f'email: {email}, template: {template}, source_ip: {source_ip}')

    try:
        response = client_dynamo.batch_write_item(
            RequestItems={
                TABLE_NAME_EMAILS: [
                    {
                        'PutRequest': {
                            'Item': _construct_email(email, template)
                        }
                    }
                ],
                TABLE_NAME_IP_ADDRESSES: [
                    {
                        'PutRequest': {
                            'Item': _construct_ip_address(source_ip)
                        }
                    }
                ]
            },
            ReturnConsumedCapacity='TOTAL',
            ReturnItemCollectionMetrics='SIZE'
        )
        logger.info(f'DynamoDB response: {response}')
        return True
    except Exception as exception:
        logger.error('Error during dynamodb put_item: %s', exception)
        return False


def get_items(email, source_ip_address):
    logger.info(f'get items for both tables - email: {email}, source_ip: {source_ip_address}')
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
    logger.info(f'dynamodb response: {response}')
    items = response['Responses']

    ip_item = _convert_ip_address(items[TABLE_NAME_IP_ADDRESSES])
    email_item = _convert_email(items[TABLE_NAME_EMAILS])

    logger.info(f'converted ip_item: {ip_item}')
    logger.info(f'converted email_item: {email_item}')
    return ip_item, email_item


def _convert_ip_address(items):
    result = _convert_common_item(items)

    if result is None:
        return None

    result['ip_address'] = items[0]['ip_address']['S']
    return result


def _convert_email(items):
    result = _convert_common_item(items)

    if result is None:
        return None

    result['email'] = items[0]['email']['S']
    result['template'] = items[0]['template']['S']
    return result


def _convert_common_item(items):
    if len(items) == 0:
        return None

    item = items[0]

    result = dict()
    result['timestamp'] = int(item['timestamp']['N'])
    result['date'] = item['date']['S']
    result['time'] = item['time']['S']
    return result


def _construct_ip_address(source_ip):
    item = _construct_common_item()
    item['ip_address'] = {'S': source_ip}
    return item


def _construct_email(email, template):
    item = _construct_common_item()
    item['email'] = {'S': email}
    item['template'] = {'S': template}
    return item


def _construct_common_item():
    date = datetime.now()
    item = {
        'timestamp': {'N': str(int(time.mktime(date.timetuple())) * 1000)},
        'date': {'S': date.strftime("%Y/%m/%d")},
        'time': {'S': date.strftime("%H:%M:%S")},
    }
    return item
