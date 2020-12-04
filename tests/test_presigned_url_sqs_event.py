"""
This file contains tests of the
"""

import pytest
import logging
import boto3
from botocore.exceptions import ClientError
import json
import os
import requests


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


def upload_file_with_presigned_url():
    """
    This function uses the presigned url returned and uploads to s3.
    :return: requests.response
    """
    fileName = 'jazz3_solo.wav'
    filePath = '{}/{}'.format('dakobedbard', fileName)
    BUCKET = 'dakobed-sqs-transform-bucket'
    response = create_presigned_post(BUCKET, filePath)

    with open(fileName, 'rb') as f:
        files = {'file': (filePath, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)
    return http_response


def test_upload_presigned_url():
    http_response = upload_file_with_presigned_url()
    assert http_response.status_code == 204
