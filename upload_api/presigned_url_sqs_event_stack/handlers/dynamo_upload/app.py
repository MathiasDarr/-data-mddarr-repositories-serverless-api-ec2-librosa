import logging
import boto3
from botocore.exceptions import ClientError
import json
import os


BUCKET = os.getenv('UploadBucket')

dynamo_endpoint = os.getenv('dynamo_endpoint')
if dynamo_endpoint == 'cloud':
    dynamo_resource = boto3.resource('dynamodb')
else:
    dynamo_resource = boto3.resource('dynamodb', endpoint_url=dynamo_endpoint)

TABLE_NAME = 'Orders'
table = dynamo_resource.Table(TABLE_NAME)


def insert_user_upload_item(upload):
    return table.put_item(
        Item={
            'user': upload['user'],
            'filename': upload['filename'],
            'fileurl': upload['fileurl'],
        }
    )

def lambda_handler(event, context):
    body = json.loads(event['body'])
    user = body['userID']
    filename = body['filename']
    user = user.split('@')[0]

    presigned = insert_user_upload_item(BUCKET, '{}/{}'.format(user, filename))
    presigned['fields']['bucket'] = BUCKET
    response = {"statusCode": 200, "body": json.dumps({
        "presigned": presigned
    }), 'headers': {"Access-Control-Allow-Origin": "*"}}
    return response

