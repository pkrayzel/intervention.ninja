import boto3
import logging
from datetime import datetime
import time
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client_dynamo = boto3.client('dynamodb')
resource_dynamo = boto3.resource('dynamodb')

TABLE_NAME_EMAILS = 'intervention_ninja_emails'
TABLE_NAME_IP_ADDRESSES = 'intervention_ninja_ips'


def store_ip_address(source_ip):
    item = _construct_common_item()
    item['ip_address'] = {'S': source_ip}
    return _put_item(TABLE_NAME_IP_ADDRESSES, item)


def store_email(email, template):
    item = _construct_common_item()
    item['email'] = {'S': email}
    item['template'] = {'S': template}
    return _put_item(TABLE_NAME_EMAILS, item)


def _construct_common_item():
    date = datetime.now()
    item = {
        'timestamp': {'N': str(int(time.mktime(date.timetuple())) * 1000)},
        'date': {'S': date.strftime("%Y/%m/%d")},
        'time': {'S': date.strftime("%H:%M:%S")},
    }
    return item


def _put_item(table_name, item):
    logger.info('Putting item into DynamoDB - table_name: {}, item: {}'.format(table_name, item))
    try:
        response = client_dynamo.put_item(
            TableName=table_name,
            Item=item
        )
        logger.info('DynamoDB response: {}'.format(response))
        return True
    except Exception as exception:
        logger.error('Error during dynamodb put_item: %s', exception)
        return False


def get_count_for_email(email, time_period_limit):
    return _get_count_for_filter(TABLE_NAME_EMAILS,
                                 'timestamp',
                                 _get_timestamp(time_period_limit),
                                 'email',
                                 email)


def get_count_for_ip_address(ip_address, time_period_limit):
    return _get_count_for_filter(TABLE_NAME_IP_ADDRESSES,
                                 'timestamp',
                                 _get_timestamp(time_period_limit),
                                 'ip_address',
                                 ip_address)


def _get_timestamp(time_period_limit):
    timestamp = int(time.mktime(datetime.now().timetuple()) * 1000) - time_period_limit
    print('time_period_limit: {}, timestamp: {}'.format(time_period_limit, timestamp))
    return timestamp


def _get_count_for_filter(table_name,
                          key_field,
                          key_value,
                          filter_field,
                          filter_value):
    logger.info('Querying DynamoDB - table_name: {}, key_field: {}, '
                'key_value: {}, filter_field: {}, filter_value: {}'
                 .format(table_name, key_field, key_value,
                         filter_field, filter_value))
    try:
        table = resource_dynamo.Table(table_name)

        response = table.scan(
            FilterExpression=Key(key_field).gt(key_value) & Attr(filter_field).eq(filter_value)
        )
        count = len(response['Items'])
        logger.info('number of items in dynamodb: {}'.format(count))
        return count
    except Exception as exception:
        logger.error('Error during dynamodb get_count_for_filter: %s', exception)
    return -1