import json
import boto3

BUCKET_NAME = 'total-code'
FILE_NAME = 'resions/all_cities.json'
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    try:
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        data = json.loads(obj['Body'].read().decode('utf-8'))

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
