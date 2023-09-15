import json
import boto3


def convert_dynamo_item(item):
    result = {}
    for key, value_data in item.items():
        for data_type, actual_value in value_data.items():
            if data_type == "S":
                result[key] = actual_value
            elif data_type == "N":
                result[key] = int(actual_value)  # 또는 float(actual_value)에 따라
    return result


def lambda_handler(event, context):
    dynamo = boto3.client("dynamodb")
    URL = "https://lvb2z5ix97.execute-api.ap-northeast-2.amazonaws.com/dev"
    client = boto3.client("apigatewaymanagementapi", endpoint_url=URL)

    msg = {"message": "Hello from server"}
    # connectionId = ["LS3IEcmXIE0CIPw=", "LS28XdYXIE0CJXA=", "LS27neQNIE0CIeg="]

    response = dynamo.scan(TableName='websocket')
    msgDB = dynamo.scan(TableName='disasterMsgDB')

    converted_data = [convert_dynamo_item(item) for item in msgDB['Items']]

    for connection in response['Items']:
        # 각 연결에 대해 DynamoDB의 전체 항목 데이터를 전송
        client.post_to_connection(ConnectionId=connection['connectionId']['S'], Data=json.dumps(converted_data))

    # for connection in response['Items']:
    #     response = client.post_to_connection(ConnectionId=connection['connectionId']['S'], Data=json.dumps(msg))

    # res_db = client.post_to_connection()
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
