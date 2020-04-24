# kinesis-s3-recovery

Recovers Kinesis Firehose source record backups from S3, replaying them into the stream.

## Installation

The python scripts make use of python 3 and boto3. `pipenv install` or `pip install boto3` will do.

## Deployment

A `package.sh` shell script will create a `lambdas.zip` that can be uploaded to AWS Lambda. The function handlers are:

  - `queue_firehose_s3_backups.main`
  - `recover_firehose_s3_backup.main`
  
The lambda functions will need an IAM role that has permissions to:
  - Read from S3
  - Put to Kinesis Firehose
  - Send and receive messages from SQS

## Functions

Files are recovered in two steps, with two lambda functions:

  1. `queue_firehose_s3_backups.py` lists all the files in the S3 source records backup and SQS queues each file
  2. `recover_firehose_s3_backup.main` is triggered by the SQS queue. It parses objects from each file and 
  puts records to the Kinesis Firehose stream

## Test

With the lambda functions deployed, they can be tested with an event like the following

### queue_firehose_s3_backups.py

```json
{
  "bucket": "my-s3-bucket",
  "prefix": "is/optional/",
  "queue_url": "https://sqs.us-east-1.amazonaws.com/123456789/my_queue.fifo",
  "kinesis_stream": "my-kinesis-stream"
}
```

The file is assumed to be formatted in the idiosyncratic Kinesis Firehose manner, with objects concatenated together.

## Credits

Thanks to Tom Chapin for the code to parse the Kinesis Firehose S3 record format:
https://stackoverflow.com/questions/34468319/reading-the-data-written-to-s3-by-amazon-kinesis-firehose-stream

## License

[MIT](LICENSE)