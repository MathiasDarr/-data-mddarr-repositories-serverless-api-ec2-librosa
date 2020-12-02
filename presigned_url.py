import logging
import boto3
from botocore.exceptions import ClientError
import json
import os
import requests

BUCKET = 'presigned-user-upload-bucket'

def create_presigned_post(bucket_name, object_name, fields=None, conditions=None, expiration=3600):
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    s3_resource= boto3.resource('s3')
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
fileName = 'profile_picture.png'
response = create_presigned_post(BUCKET, fileName)

# fields = presigned['fields']
# access_key = fields['AWSAccessKeyId']
# signature = fields['signature']
# key = fields['key']
# url = presigned['url']
# expires = '2147483647'
# parsed_presigned_url = url + key + '?AWSAccessKeyId=' +access_key +'&Expires=' +expires +'&Signature=' + signature
# print(parsed_presigned_url)


with open(fileName, 'rb') as f:
    files = {'file': (fileName, f)}
    http_response = requests.post(response['url'], data=response['fields'], files=files)