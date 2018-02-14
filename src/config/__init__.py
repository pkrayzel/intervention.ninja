import boto3


def is_local(env):
    """Return True if we're running in a local env, otherwise False"""
    return env.get('ENV', 'local') == 'local'


def get_aws_config(env):
    return {
        'aws_access_key_id': env.get('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': env.get('AWS_SECRET_ACCESS_KEY'),
        'region_name': env.get('AWS_REGION', 'us-east-1')
    }


def make_dynamodb_client(env):
    default_endpoint = 'http://localhost:4572' if is_local(env) else None
    endpoint_url = env.get('HACIENDA_S3_ENDPOINT_URL', default_endpoint)

    return boto3.client('s3', endpoint_url=endpoint_url, **get_aws_config(env))


def make_sns_client(env):
    default_endpoint = 'http://localhost:4576' if is_local(env) else None
    endpoint_url = env.get('HACIENDA_SQS_ENDPOINT_URL', default_endpoint)
    return boto3.client('sns', endpoint_url=endpoint_url, **get_aws_config(env))


def get_sns_topic_name(env):
    return env.get('HACIENDA_SQS_QUEUE_URL', None)


def get_email_config(env):
    if is_local(env):
        host = env.get('HACIENDA_EMAIL_HOST', 'mail')
        port = int(env.get('HACIENDA_EMAIL_PORT', 1025))
    else:
        host = env.get('NOMAD_IP_hacienda_ses_smtp')
        port = int(env.get('NOMAD_PORT_hacienda_ses_smtp'))

    return {
        'host': host,
        'port': port,
        'from_addr': env.get(
            'HACIENDA_EMAIL_FROM', 'no-reply-hacienda@made-test.com'
        ),
    }
