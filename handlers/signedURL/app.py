import logging
import boto3
from botocore.exceptions import ClientError
import json
import os

BUCKET = os.getenv('UploadBucket')


def create_presigned_post(bucket_name, object_name, fields=None, conditions=None, expiration=3600):
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


def lambda_handler(event, context):

    presigned = create_presigned_post(BUCKET, 'user_upload.png')
    response = {"status_code": 200, "body": json.dumps({
        "presigned": presigned
    }), 'headers': {
        "Access-Control-Allow-Origin": "*",
        "X-Requested-With": '*',
        "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',
        "Access-Control-Allow-Methods": 'POST,GET,OPTIONS'
    }}

    return response