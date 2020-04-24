mkdir lib
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t lib
zip -r lambdas.zip lib
zip -g lambdas.zip queue_firehose_s3_backups.py
zip -g lambdas.zip recover_firehose_s3_backup.py
