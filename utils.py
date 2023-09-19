import time
from datetime import datetime

def get_expiration_time(disaster_type):
    current_time = int(time.time())
    ttl_values = {
        "태풍": 18000,   # 5 hour
        "산사태": 18000,   # 5 hour
        "홍수": 14400,   # 4 hour
        "호우": 21600,   # 6 hour
        "폭염": 21600,   # 6 hour
        "대설": 21600,   # 6 hour
        "지진": 18000,   # 5 hour
        "강풍": 14400,   # 4 hour
        "교통사고": 7200,   # 2 hour
        "화재": 10800,   # 3 hour
        # "화재": 60,   # 3 hour
        "산불": 21600,  # 6 hours
        "교통통제": 7200,   # 2 hour
        "지진해일": 21600,   # 6 hour
        "기타": 10800,   # 3 hour
        "실종": 21600   # 6 hours
    }
    return current_time + ttl_values.get(disaster_type, 10800)  # default: 3 hour

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')