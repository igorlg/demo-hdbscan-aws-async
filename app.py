import os
import json
from decimal import Decimal
from uuid import uuid4

# AWS
import boto3
import pandas as pd
# Utils
from utils import EC2Meta


aws_region = os.environ['AWS_REGION']
sqs = boto3.client('sqs', region_name=aws_region)
s3 = boto3.client('s3', region_name=aws_region)
ddb_res = boto3.resource('dynamodb', region_name=aws_region)

# SQS
sqs_timeout = 20
req_queue_url = os.environ['SQS_REQUEST_QUEUE_URL']

# S3
data_file = os.environ['S3_DATA_FILE_NAME']
s3_bucket = os.environ['S3_BUCKET_NA<E']
s3_data_file = os.path.join('data', data_file)
local_data_path = os.environ['LOCAL_DATA_PATH']
local_data_file = os.path.join(local_data_path, data_file)

# DynamoDB
ddb_result_table = os.environ['DDB_RESULT_TABLE_NAME']
ddb_metrics_table = os.environ['DDB_METRIC_TABLE_NAME']
ddb_result = ddb_res.Table(ddb_result_table)


def put_metric(algo, operation, n_points, duration):
    item = {'ObjectId': str(uuid4()),
            'Algorithm': algo.upper(),
            'InstanceType': EC2Meta.instance_type(),
            'Operation': operation,
            'NumPoints': Decimal(n_points),
            'Duration': Decimal(duration),
            }
    tab = ddb_res.Table(ddb_metrics_table)
    tab.put_item(Item=item)


def get_data_source():
    if not os.access(local_data_file, os.R_OK):
        s3.download_file(s3_bucket, s3_data_file, local_data_file)

    data = pd.read_csv(local_data_file)
    return data


def dequeue():
    m = None

    while True:
        resp = sqs.receive_message(QueueUrl=req_queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=sqs_timeout)
        if resp.get('Messages', None) is not None:
            break

    try:
        m = resp['Messages'][0]
        handle = m['ReceiptHandle']
        sqs.delete_message(QueueUrl=req_queue_url, ReceiptHandle=handle)

        return json.loads(m['Body'])
    except KeyError:
        return None
    except json.decoder.JSONDecodeError:
        return None


def upload_results(req_id, img_file, csv_file):
    s3_img_result_file = os.path.join('results', os.path.basename(img_file))
    s3_csv_result_file = os.path.join('results', os.path.basename(csv_file))

    ddb_result_item = {'RequestId': req_id,
                       'ImageLocalFile': img_file,
                       'ImageS3File': {'key': s3_img_result_file, 'bucket': s3_bucket},
                       'CSVLocalFile': csv_file,
                       'CSVS3File': {'key': s3_csv_result_file, 'bucket': s3_bucket},
                       }

    s3.upload_file(img_file, s3_bucket, s3_img_result_file)
    s3.upload_file(csv_file, s3_bucket, s3_csv_result_file)
    ddb_result.put_item(Item=ddb_result_item)
    os.remove(img_file)


def main(msg):
    # Decode SQS Request Msg
    request_id = msg['RequestId']  # msg['RequestId'] to track requests...
    algorithm = msg.get('Algorithm', 'OPTICS')
    number_of_points = msg.get('NumberOfPoints', 25000)
    local_img_file = os.path.join(local_data_path, '{}.png'.format(request_id))
    local_csv_file = os.path.join(local_data_path, '{}.csv'.format(request_id))

    # Run Algorithm
    cluster_points = calculate_cluster(data=df, n_points=number_of_points, algo=algorithm)
    gen_results(cluster_points, local_img_file, local_csv_file,
                'Full data set vs {} reduced set'.format(algorithm.upper()))
    upload_results(request_id, local_img_file, local_csv_file)


if __name__ == '__main__':
    df = get_data_source()

    while True:
        message = dequeue()
        if message is None or message.get('RequestId', None) is None:
            continue

        main(message)
