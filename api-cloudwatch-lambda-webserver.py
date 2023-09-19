import json
import boto3
import requests
import time
from datetime import datetime
from utils import get_expiration_time, get_current_time
from dynamodb_operations import check_db, save_to_db
from http_requests import get_basic_info
from decimal import Decimal


def get_manual_from_s3(bucket_name, file_name, disaster_type):
    s3 = boto3.client('s3')
    print(disaster_type)
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    content = obj['Body'].read().decode('utf-8')
    data = json.loads(content)
    print(data)
    # Check for the specific disaster type and if not found, default to "기타"
    return data.get(disaster_type, data.get("기타", ""))


def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')

    function_name_pandas = 'pandas_test'
    function_name_selenium = 'getDisMsgSelenium'

    try:
        basic_info = get_basic_info()
        md101_sn = basic_info.get('md101_sn')

        if not check_db(md101_sn):
            payload_selenium = {}

            response_selenium = lambda_client.invoke(
                FunctionName=function_name_selenium,
                InvocationType='RequestResponse',  # 'RequestResponse' (동기) 또는 'Event' (비동기)
                Payload=json.dumps(payload_selenium)
            )

            res_selenium = json.loads(response_selenium['Payload'].read())
            if res_selenium['statusCode'] == 200:
                additional_info = res_selenium['body']
                basic_info.update(additional_info)

            else:
                # 오류 처리
                return {
                    'statusCode': 500,
                    'body': json.dumps("Failed to get additional info.")
                }

            if '실종' in basic_info['msg']:
                basic_info['disaster_type'] = '실종'

            disaster_type = basic_info.get('disaster_type', '')
            basic_info['stored_time'] = get_current_time()
            basic_info['expiration_time'] = get_expiration_time(disaster_type)

            manual = get_manual_from_s3('dis-menual', 'menual.json', disaster_type)
            print("여기!!!")
            print(manual)

            if manual:
                basic_info['manual'] = manual

            payload_pandas = {
                'location_name': basic_info['location_name']
            }

            response_pandas = lambda_client.invoke(
                FunctionName=function_name_pandas,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload_pandas)
            )

            res_code = json.loads(response_pandas['Payload'].read())
            location_code = res_code['body']['location_code']
            coordinate = res_code['body']['coordinate']
            basic_info['location_code'] = location_code
            basic_info['coordinate'] = [[Decimal(str(val)) for val in inner_list] for inner_list in coordinate]

            save_to_db(basic_info)

        return {
            'statusCode': 200,
            'body': json.dumps('Process Complete!')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Unknown error occurred: {str(e)}")
        }