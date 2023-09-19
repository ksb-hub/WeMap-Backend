import pandas as pd
import boto3
import io
import ast


def lambda_handler(event, context):
    print(event)
    # 초기 변수 설정
    BUCKET_NAME = 'total-code'  # S3 버킷 이름
    FILE_NAME = 'total_code_revised.xlsx'  # S3에 저장된 Excel 파일 이름

    # location_name = '서울특별시' # 요청에서 location_name 추출
    location_name = event['location_name']

    # 강원도 -> 강원특별자치도
    location_name = location_name.replace('강원특별자치도', '강원도')

    print(location_name)

    if not location_name:
        return {
            'statusCode': 400,
            'body': 'location_name is required in the request'
        }

    # S3에서 Excel 파일을 읽어옵니다
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    data = obj['Body'].read()

    # 데이터를 pandas dataframe으로 로드합니다
    df = pd.read_excel(io.BytesIO(data))

    # location_name에 해당하는 location_code 찾기
    location_name_list = location_name.split(',')
    print(location_name)
    location_code_list = []
    coordinate_list = []

    for location_name in location_name_list:
        location_code = df[df['병합_명칭'] == location_name]['병합_코드'].values
        print("location_code: ", location_code)
        coordinate = ast.literal_eval(df[df['병합_명칭'] == location_name]['중앙_좌표'].values[0])
        if len(location_code) > 0 and len(coordinate) > 0:
            location_code_list.append(int(location_code[0]))
            coordinate_list.append(list(coordinate))

    print(coordinate_list)

    # 결과 확인
    if len(location_code_list) == 0:
        return {
            'statusCode': 404,
            'body': f'No location_code found for {location_name}'
        }

    return {
        'statusCode': 200,
        'body': {
            'location_name': location_name,
            'location_code': location_code_list,
            'coordinate': coordinate_list
        }
        # 'statusCode': 200,
        # 'body': 'Hello! from pandas_test'
    }

    # def get_location_code_from_excel(location_name, s3_client, BUCKET_NAME, FILE_NAME):
    # s3_client = boto3.client('s3')
    # BUCKET_NAME = 'total-code'
    # FILE_NAME = 'total_code.xlsx'
    # obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    # data = obj['Body'].read()
    # df = pd.read_excel(io.BytesIO(data))
    # location_code = df[df['병합_명칭'] == location_name]['병합_코드'].values
