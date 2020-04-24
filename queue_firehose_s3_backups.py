"""Recovers Kinesis S3 source record backup files, queueing each file to be proessed by recover_firehose_s3_backup.py"""
import boto3
import json


def main(event, context):
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')

    if 'prefix' in event:
        listing = s3.list_objects_v2(Bucket=event['bucket'], Prefix=event['prefix'])
    else:
        listing = s3.list_objects_v2(Bucket=event['bucket'])

    if listing['IsTruncated']:
        print("WARNING: S3 bucket listing was truncated")

    messages = []
    bucket = listing['Name']
    for obj in listing['Contents']:
        if not obj['Key'].endswith('/'):
            message = {
                'Id': str(len(messages) + 1),
                'MessageBody': json.dumps({
                    'bucket': bucket,
                    'item': obj['Key'],
                    'kinesis_stream': event['kinesis_stream']
                }),
                'MessageGroupId': event['bucket']
            }
            messages.append(message)
            if len(messages) == 10:
                sqs.send_message_batch(
                    QueueUrl=event['queue_url'],
                    Entries=messages)
                messages = []

    if len(messages) > 0:
        sqs.send_message_batch(
            QueueUrl=event['queue_url'],
            Entries=messages)
