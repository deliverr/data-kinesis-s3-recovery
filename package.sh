mkdir lib
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t lib
zip -r lambda.zip lib
zip -g lambda.zip recover_firehose_s3_backup.py