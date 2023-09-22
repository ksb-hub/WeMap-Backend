import boto3
import hashlib

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')


def lambda_handler(event, context):
    # DynamoDB에서 사용자 정보 검색
    response = table.get_item(Key={'email': event['email']})
    user = response.get('Item')
    if not user:
        return {
            'statusCode': 404,
            'body': {"message": "User not found"}
        }

    # 입력된 비밀번호와 저장된 비밀번호 비교
    # salt_bytes = user['salt'].value  # 바이트로 변환
    # print("salt Error!!!!!")
    # print(salt_bytes)
    # hashed_password = hashlib.pbkdf2_hmac('sha256', event['password'].encode(), salt_bytes, 100000)
    # print(hashed_password)

    print(user['password'])

    if event['password'] == user['password']:  # 비밀번호도 바이트로 변환하여 비교
        return {
            "statusCode": 200,
            "body": {
                "message": "Login successful",
                "dis_level": user['dis_level']
            }
        }
    else:
        return {
            'statusCode': 404,
            'body': {"message": "Password Wrong"}
        }
