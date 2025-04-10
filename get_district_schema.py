import pandas as pd
import json
import os

def tuple_string_to_list(tuple_string):
    """문자열 형태의 튜플을 리스트로 변환"""
    return list(map(float, tuple_string.strip("()").split(',')))

def convert_df_to_json(df):
    cities = {}
    for index, row in df.iterrows():
        location_name = row['merged_location_name']
        location_code = row['merged_location_code']
        coordinate = tuple_string_to_list(row['median_coordinate'])
        parts = location_name.split()

        # 시 처리
        if len(parts) == 1 or parts[0] not in cities:
            cities.setdefault(parts[0], {
                "code": location_code,
                "coordinate": coordinate,
                "군구": {}
            })

        # 시+구 처리
        if len(parts) >= 2:
            cities[parts[0]]["군구"].setdefault(parts[1], {
                "code": location_code,
                "coordinate": coordinate
            })

        # 시+구+동 처리
        if len(parts) == 3:
            cities[parts[0]].setdefault("읍면동", {}).setdefault(parts[1], {}).setdefault(parts[2], {
                "code": location_code,
                "coordinate": coordinate
            })

    return cities

df = pd.read_excel('../code_test/total_code_revised.xlsx', header=0, dtype=str)

cities_data = convert_df_to_json(df)

# 전체 시도를 포함하는 JSON 파일 저장
with open('all_cities.json', 'w', encoding='utf-8') as f:
    json.dump({city: {"code": city_data["code"], "coordinate": city_data["coordinate"]} for city, city_data in cities_data.items()}, f, ensure_ascii=False, indent=4)

# 각 시별 구 전체의 JSON 파일 저장
for city, city_data in cities_data.items():
    with open(f'{city_data["code"]}.json', 'w', encoding='utf-8') as f:
        json.dump({district: {"code": data["code"], "coordinate": data["coordinate"]} for district, data in city_data["군구"].items()}, f, ensure_ascii=False, indent=4)

    # 각 구별 전체의 동 JSON 파일 저장
    for district, district_data in city_data["군구"].items():
        if "읍면동" in city_data and district in city_data["읍면동"]:
            filename = f"{district_data['code']}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({town: {"code": data["code"], "coordinate": data["coordinate"]} for town, data in city_data["읍면동"][district].items()}, f, ensure_ascii=False, indent=4)
