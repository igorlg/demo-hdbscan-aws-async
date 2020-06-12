# demo-hdbscan-aws-async


## Example of SQS Message:
```
{
  "RequestId": "xxxxxxxx",
  "Algorithm": "xxx",
  "NumberOfPoints": 100000
}
```

## MANDATORY ENVIRONMENT VARIABLES
* SQS_REQUEST_QUEUE_URL
* S3_DATA_FILE_NAME
* S3_BUCKET_NAME
* DDB_RESULT_TABLE_NAME
* DDB_METRIC_TABLE_NAME
