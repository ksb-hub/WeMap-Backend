import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('disasterMsgDB')

def check_db(md101_sn):
    existing_item = table.get_item(Key={'md101_sn': md101_sn})
    return 'Item' in existing_item

def save_to_db(item):
    table.put_item(Item=item)