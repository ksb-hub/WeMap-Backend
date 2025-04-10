import json
import boto3
import hashlib
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')


# def hash_password(password):
#     salt = os.urandom(16)
#     hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
#     return {
#         'salt': salt,
#         'hashed_password': hashed
#     }

def check_db(email):
    existing_item = table.get_item(Key={'email': email})
    return 'Item' in existing_item


def signup(event, context):
    # password_data = hash_password(event['password'])
    # password_data = event['password']

    table.put_item(
        Item={
            'email': event['email'],
            'password': event['password'],
            # 'salt': password_data['salt'],
            'dis_level': event['dis_level']
        }
    )

    return {"message": "User registered successfully"}


def lambda_handler(event, context):
    print(event)
    email = event['email']
    if check_db(email):
        return {
            'statusCode': 500,
            'body': json.dumps({"message": "User registered successfully"})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(signup(event, context))
    }
