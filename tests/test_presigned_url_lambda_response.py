"""


"""
import logging
import boto3
from botocore.exceptions import ClientError
import requests


# user = 'dakobedbard'
# BUCKET = 'dakobed-sqs-transform-bucket'
# key = '{}/{}'.format(user, fileName)


# presigned_post_url = response_body['url']
# access_key = response_body['fields']['AWSAccessKeyId']
# policy = response_body['fields']['policy']
# signature = response_body['fields']['signature']


url = 'https://ygn5tdcdh1.execute-api.us-west-2.amazonaws.com/Prod/signedURL'

def create_presigned_post(bucket_name, object_name, fields=None, conditions=None, expiration=3600):
    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    s3_resource = boto3.resource('s3')
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



def test_upload_file_with_presigned_url_received_from_lambda():
    """
    This function uses the presigned url returned and uploads to s3.
    :return: requests.response
    """
    filename = "jazz3_solo.wav"
    userID = "dakobedbard@gmail.com"

    body = {"filename": filename, "userID": userID}
    lambda_presigned_post = requests.post(url, json=body)

    assert lambda_presigned_post.status_code == 200

    response_body = lambda_presigned_post.json()['presigned']
    fields = response_body['fields']
    del fields['x-amz-security-token']
    response = {'url':response_body['url'], 'fields': fields}
    return response


fileName = 'jazz3_solo.wav'
user = 'dakobedbard'
BUCKET = 'dakobed-sqs-transform-bucket'
key = '{}/{}'.format(user, fileName)
# response = create_presigned_post(BUCKET, key)
response = test_upload_file_with_presigned_url_received_from_lambda()

with open(fileName, 'rb') as f:
    files = {'file': (fileName, f)}
    http_response = requests.post(response['url'], data=response['fields'], files=files)

