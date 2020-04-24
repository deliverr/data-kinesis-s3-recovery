"""Recovers a single s3 file: Decodes objects and puts them to Kinesis stream"""
import base64
import boto3
import json
from json.decoder import JSONDecodeError


def main(event, context):
    s3 = boto3.resource('s3')
    for record in event['Records']:
        s3_listing = json.loads(record['body'])
        s3_obj = s3.Object(s3_listing['bucket'], s3_listing['item'])
        content = s3_obj.get()['Body'].read().decode('utf-8')

        decoder = json.JSONDecoder()
        content_length = len(content)
        decode_index = 0

        firehose = boto3.client('firehose')
        while decode_index < content_length:
            try:
                obj, decode_index = decoder.raw_decode(content, decode_index)
                serialized = base64.b64encode(
                    json.dumps(obj)
                        .encode('utf-8'))
                firehose.put_record(
                    DeliveryStreamName=s3_listing['kinesis_stream'],
                    Record={
                        'Data': serialized
                    }
                )
            except JSONDecodeError as e:
                # Scan forward and keep trying to decode
                decode_index += 1
