#!/bin/bash

docker run -d \
  -e SQS_REQUEST_QUEUE_URL="" \
  -e S3_DATA_FILE_NAME="" \
  -e S3_BUCKET_NAME="" \
  -e DDB_RESULT_TABLE_NAME="" \
  -e DDB_METRIC_TABLE_NAME="" \
demo-hdbscan-aws-async
