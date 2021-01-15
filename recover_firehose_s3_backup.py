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
        # print(f"content length {len(content)}, first 512: {content[:512]}")

        decoder = json.JSONDecoder()
        decode_index = 0

        firehose = boto3.client('firehose')
        while decode_index < len(content):
            try:
                obj, decode_index = decoder.raw_decode(content, decode_index)
                # print(obj)
                if 'errorCode' in obj and 'attemptsMade' in obj and 'rawData' in obj:
                    # recovering from ProcessingFailed records
                    bytes = base64.b64decode(obj['rawData'])
                else:
                    # recovering from source records
                    bytes = json.dumps(obj).encode('utf-8')
                firehose.put_record(
                    DeliveryStreamName=s3_listing['kinesis_stream'],
                    Record={
                        'Data': bytes
                    }
                )
                content = content[decode_index:]
                decode_index = 0
            except JSONDecodeError as e:
                # Scan forward and keep trying to decode
                decode_index += 1
