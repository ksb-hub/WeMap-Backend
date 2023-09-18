import json
import boto3
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('disasterMsgDB')  # DynamoDB 테이블 이름으로 바꾸십시오.


def checkDB(md101_sn):
    existing_item = table.get_item(Key={'md101_sn': md101_sn})
    return 'Item' in existing_item


def getbasicInfo():
    response = requests.get(
        'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?ServiceKey=jabqrH9wuN4m67rfaVV2Iy1EEYwKfvUDJL1TGqL4K51ifViX8uBIYpfSiTTfH6P%2F3kxwcdZEoOXCDMZrrcfWuA%3D%3D&type=json&pageNo=1&numOfRows=1')
    response.raise_for_status()
    data = response.json()
    item = data['DisasterMsg'][1]['row'][0]
    return item


def getAdditionalinfo():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = "/opt/python/bin/headless-chromium"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/opt/python/bin/chromedriver')
    URL = "https://www.safekorea.go.kr/idsiSFK/neo/sfk/cs/sfc/dis/disasterMsgList.jsp?menuSeq=679"
    data_dict = {}

    try:
        driver.get(URL)
        # 페이지의 첫 번째 요소가 로드될 때까지 최대 10초간 대기합니다.
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "disasterSms_tr_0_apiData1"))
        )

        disaster_type = driver.find_element(By.ID, f"disasterSms_tr_0_DSSTR_SE_NM").text
        emergency_step = driver.find_element(By.ID, f"disasterSms_tr_0_EMRGNCY_STEP_NM").text

        data_dict = {
            "disaster_type": disaster_type,
            "emergency_step": emergency_step,
        }

    except WebDriverException as e:
        print(f"Selenium Error: {str(e)}")

    finally:
        driver.quit()

    return data_dict


def get_expiration_time(disaster_type):
    current_time = int(time.time())
    ttl_values = {
        "태풍": 18000,  # 5 hour
        "산사태": 18000,  # 5 hour
        "홍수": 14400,  # 4 hour
        "호우": 21600,  # 6 hour
        "폭염": 21600,  # 6 hour
        "대설": 21600,  # 6 hour
        "지진": 18000,  # 5 hour
        "강풍": 14400,  # 4 hour
        "교통사고": 7200,  # 2 hour
        "화재": 10800,  # 3 hour
        # "화재": 60,   # 3 hour
        "산불": 21600,  # 6 hours
        "교통통제": 7200,  # 2 hour
        "지진해일": 21600,  # 6 hour
        "기타": 10800,  # 3 hour
        "실종": 21600  # 6 hours
    }
    return current_time + ttl_values.get(disaster_type, 10800)  # default: 3 hour


def lambda_handler(event, context):
    lambda_client = boto3.client('lambda')

    function_name = 'pandas_test'

    try:
        basic_info = getbasicInfo()
        md101_sn = basic_info.get('md101_sn')

        if not checkDB(md101_sn):
            additional_info = getAdditionalinfo()
            basic_info.update(additional_info)

            if '실종' in basic_info['msg']:
                basic_info['disaster_type'] = '실종'
            basic_info['stored_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # basic_info['stored_time'] = int(time.time())
            basic_info['expiration_time'] = get_expiration_time(basic_info.get('disaster_type', ''))

            payload = {
                'location_name': basic_info['location_name']
            }

            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',  # 'RequestResponse' (동기) 또는 'Event' (비동기)
                Payload=json.dumps(payload)
            )

            res_code = json.loads(response['Payload'].read())
            print(res_code)
            location_code = res_code['body']['location_code']
            basic_info['location_code'] = location_code

            table.put_item(Item=basic_info)

        return {
            'statusCode': 200,
            'body': json.dumps('Process Complete!')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Unknown error occurred: {str(e)}")
        }