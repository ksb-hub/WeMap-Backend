import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

def lambda_handler(event, context):
    response = table.get_item(Key={'email': event['email']})
    user = response.get('Item')
    if not user:
        return {"message": "User not found"}, 404
    return {"dis_level": user['dis_level']}
