import requests
import asyncio
from datetime import datetime, timezone
from switch_code import response_XY
import numpy as np

REACT_APP_MAP_CLIENT_ID = "c80d004ef85c4d00988b"
REACT_APP_MAP_SECRET_ID = "6d1ed811689e4f6ab43d"
baseURL = "https://sgisapi.kostat.go.kr/OpenAPI3/"

access_token = None
access_expire = None

async def get_access():
    api_url = baseURL + "/auth/authentication.json"
    try:
        response = requests.get(api_url, params={
            "consumer_key": REACT_APP_MAP_CLIENT_ID,
            "consumer_secret": REACT_APP_MAP_SECRET_ID
        })
        data = response.json()
        global access_token, access_expire
        access_token = data["result"]["accessToken"]
        access_expire = data["result"]["accessTimeout"]
    except Exception as e:
        print(f"Error: {e}")


def get_current_time_in_seconds():
    now = datetime.now(timezone.utc)
    return int(now.timestamp())

async def map_refresh():
    current_time_in_seconds = get_current_time_in_seconds()

    global access_token, access_expire
    if access_token:
        if current_time_in_seconds > int(access_expire):
            await get_access()
    else:
        await get_access()

async def get_geo_boundary(geoCode):
    await map_refresh()
    api_url = baseURL + "/boundary/hadmarea.geojson"
    request_data = {
        "accessToken": access_token,
        "year": 2022,
        "adm_cd": geoCode,
        "low_search": 0
    }
    try:
        response = requests.get(api_url, params=request_data)
        data = response.json()
        if data["features"][0]["geometry"]["type"] == "MultiPolygon":
            multi_bound = data["features"][0]["geometry"]["coordinates"]
            result = []
            for element in multi_bound:
                multi_child = element[0]
                result_child = [list(reversed(coord)) for coord in multi_child]
                result.append(result_child)
            print("MultiPolygon coordinates:")
            # print(result)
            return result
        else:
            vertex = data["features"][0]["geometry"]["coordinates"][0]
            result_list = [list(reversed(coord)) for coord in vertex]
            print("Single coordinates:")
            # print(result_list)
            return [result_list]
    except Exception as e:
        print(f"Error with administrative code: {request_data['adm_cd']}")
        print(f"Error: {e}")
        return []


def main():
    geo_code_example = "39"  # 예시로 사용할 지역코드를 여기에 넣어주세요.

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_geo_boundary(geo_code_example))
    loop.close()

    X_list = [XY[0] for f_item in result for XY in f_item]
    Y_list = [XY[1] for f_item in result for XY in f_item]

    XY_dict = {'X_list': X_list, 'Y_list': Y_list}

    res = response_XY(XY_dict=XY_dict)

    print(res[:10])


if __name__ == "__main__":
    main()
