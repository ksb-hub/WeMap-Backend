import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')


def lambda_handler(event, context):
    table.update_item(
        Key={'email': event['email']},
        UpdateExpression="set dis_level = :r",
        ExpressionAttributeValues={':r': event['dis_level']},
        ReturnValues="UPDATED_NEW"
    )

    return {"message": "User updated successfully"}
