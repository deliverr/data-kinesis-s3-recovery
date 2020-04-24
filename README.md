# kinesis-s3-recoverry

Recovers Kinesis Firehose source record backups from S3, replaying them into the stream.

## Installation

The python script makes use of python 3 and boto3. `pipenv install` or `pip install boto3` will do.

## Deployment

A `package.sh` shell script will create a `lambdas.zip` that can be uploaded to AWS Lambda. The function handlers are:

  - `queue_firehose_s3_backups.py`
  - `recover_firehose_s3_backup.main`
  
`recover_firehose_s3_backup.py` reads a file from S3 and puts objects to a Kinesis Firehose stream.

The lambda function will need an IAM role that has permissions to read from S3 and put to Kinesis Firehose.

## Functions

Files are recovered in two steps, with two lambda functions:

  1. List all the files in the S3 source records backup and SQS queue each file
  2. Parse objects from each file and put records to Kinesis Firehose stream

## Test
With the lambda functions deployed, they can be tested with an events like the following

### queue_firehose_s3_backups.py

```json
{
  "bucket": "my-s3-bucket",
  "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789/my_queue.fifo",
  "kinesis_stream": "my-kinesis-stream"
}
```

### recover_firehose_s3_backup.py

```json
{
    "Records": [{
        "body": {
          "bucket": "my-s3-bucket",
          "item": "path/to/my-s3-source-record-backup",
          "kinesis_stream": "my-kinesis-stream"
        }
    }]
} 
```

The file is assumed to be formatted in the idiosyncratic Kinesis Firehose manner, with objects concatenated together.

## Credits

Thanks to Tom Chapin for the code to parse the Kinesis Firehose S3 record format:
https://stackoverflow.com/questions/34468319/reading-the-data-written-to-s3-by-amazon-kinesis-firehose-stream