import requests
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.blocking import BlockingScheduler

# 전역 변수로 최근 응답의 md101_sn을 저장
last_md101_sn = None


def job():
    global last_md101_sn

    url = "http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List?ServiceKey=jabqrH9wuN4m67rfaVV2Iy1EEYwKfvUDJL1TGqL4K51ifViX8uBIYpfSiTTfH6P%2F3kxwcdZEoOXCDMZrrcfWuA%3D%3D&type=json&pageNo=1&numOfRows=1"

    response = requests.get(url)

    try:
        data = response.json()
        latest_msg = data["DisasterMsg"][1]["row"][0]  # 최근 메시지
        current_md101_sn = latest_msg["md101_sn"]

        # md101_sn이 이전과 동일한지 확인
        if current_md101_sn == last_md101_sn:
            print("대기중")
        else:
            print(latest_msg)
            last_md101_sn = current_md101_sn
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON from API response.")
    except KeyError:
        print("Unexpected data format from API.")


def main():
    sched = BlockingScheduler()
    try:
        sched.remove_job('test')  # 기존에 등록된 작업 제거 (오류 회피 목적)
    except JobLookupError:
        pass
    sched.add_job(job, 'interval', seconds=5, id='test', max_instances=2)
    sched.start()