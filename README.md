# kinesis-s3-recoverry

Recovers Kinesis Firehose source record backups from S3, replaying them into the stream.

## Installation

The python script makes use of python 3 and boto3. `pipenv install` or `pip install boto3` will do.

## Deployment

A `package.sh` shell script will create a `lambdas.zip` that can be uploaded to AWS Lambda. The function handlers are:

  - [TODO] list s3 bucket to SQS messages
  - `recover_firehose_s3_backup.main`
  
`recover_firehose_s3_backup.py` reads a file from S3 and puts objects to a Kinesis Firehose stream.

The lambda function will need an IAM role that has permissions to read from S3 and put to Kinesis Firehose.

## Test

With the lambda function deployed, it can be tested with an event like:

```json
{ 
  "bucket": "my-s3-bucket", 
  "item": "path/to/my-s3-source-record-backup", 
  "kinesis_stream": "my-kinesis-stream" 
}
```

The file is assumed to be formatted in the idiosyncratic Kinesis Firehose manner, with objects concatenated together.

## Credits

Thanks to Tom Chapin for the code to parse the Kinesis Firehose S3 record format:
https://stackoverflow.com/questions/34468319/reading-the-data-written-to-s3-by-amazon-kinesis-firehose-stream