import json
import boto3

def lambda_handler(event, context):
    qs = event.get('queryStringParameters').get('token')
    print(qs)
    client = boto3.client("dynamodb")
    client.put_item(TableName="websocket", Item={"connectionId": {"S": event['requestContext'].get("connectionId")},
                                                "token": {"S": qs}})
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
