import json
import boto3

BUCKET_NAME = 'total-code'  # S3 버킷 이름
BASE_FILE_NAME = 'resions/'
s3_client = boto3.client('s3')

def get_data_from_s3_json(code):
    try:
        obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=BASE_FILE_NAME + code + '.json')
        return json.loads(obj['Body'].read().decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Failed to retrieve data for code {code}. Error: {str(e)}")

def lambda_handler(event, context):
    code = event.get('code')
    if not code:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': 'code parameter is missing'})
        }

    try:
        data = get_data_from_s3_json(code)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(data)
        }
    except ValueError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
