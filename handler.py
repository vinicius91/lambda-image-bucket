import boto3
import json
import os
import cStringIO
import decimal
from PIL import Image
from PIL.ExifTags import TAGS

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client('s3')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)


def get_s3_image_info(bucket, key):
    res = s3.get_object(Bucket=bucket, Key=key)
    imagecontent = res['Body'].read()

    file = cStringIO.StringIO(imagecontent)
    img = Image.open(file)

    return img.size


def extractMetadata(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    size = event['Records'][0]['s3']['object']['size']
    width, height = get_s3_image_info(bucket, key)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        's3objectkey': key,
        'bucket': bucket,
        'size': size,
        'width': width,
        'height': height,
    }
    table.put_item(Item=item)
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    print(response)


def getMetadata(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    print(event)
    key = event['pathParameters']['s3objectkey'].replace('%2F', '/')
    # fetch todo from the database
    result = table.get_item(
        Key={
            's3objectkey': key
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'], cls=DecimalEncoder)
    }

    return response
