import requests

SERVICE_URL = 'http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?ServiceKey=jabqrH9wuN4m67rfaVV2Iy1EEYwKfvUDJL1TGqL4K51ifViX8uBIYpfSiTTfH6P%2F3kxwcdZEoOXCDMZrrcfWuA%3D%3D&type=json&pageNo=1&numOfRows=1'

def get_basic_info():
    response = requests.get(SERVICE_URL)
    response.raise_for_status()
    data = response.json()
    item = data['DisasterMsg'][1]['row'][0]
    return item