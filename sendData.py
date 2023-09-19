import json
import boto3


def convert_dynamo_item(item):
    result = {}
    for key, value_data in item.items():
        if not isinstance(value_data, dict):
            continue

        for data_type, actual_value in value_data.items():
            if data_type == "S":
                result[key] = actual_value
            elif data_type == "N":
                result[key] = float(actual_value) if "." in actual_value else int(actual_value)
            elif data_type == "L":
                if key == "coordinate":
                    # Handle nested list for coordinates
                    result[key] = []
                    for sublist in actual_value:
                        coords = []
                        for coord_list in sublist.get("L", []):
                            for coord_key, coord_val in coord_list.items():
                                if coord_key == "N":
                                    coords.append(float(coord_val))
                        result[key].append(coords)
                else:
                    # Handle simple list items (e.g., location_code)
                    result[key] = [val[list(val.keys())[0]] for val in actual_value]
    return result


def lambda_handler(event, context):
    dynamo = boto3.client("dynamodb")
    URL = "https://lvb2z5ix97.execute-api.ap-northeast-2.amazonaws.com/dev"
    client = boto3.client("apigatewaymanagementapi", endpoint_url=URL)

    response = dynamo.scan(TableName='websocket')
    msgDB = dynamo.scan(TableName='disasterMsgDB')

    converted_data = [convert_dynamo_item(item) for item in msgDB['Items']]

    for connection in response['Items']:
        # 각 연결에 대해 DynamoDB의 전체 항목 데이터를 전송
        client.post_to_connection(ConnectionId=connection['connectionId']['S'], Data=json.dumps(converted_data))

    print("sendData 실행!!!!")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
