import pandas as pd
import json
import os


def load_and_process_data(filepath):
    with open(filepath, encoding='utf-8') as f:
        js = json.loads(f.read())
    df = pd.DataFrame(js)

    df['FACIL_X'] = (df['FACIL_LADE'] + df['FACIL_LAMI'] / 60 + df['FACIL_LASE'] / 3600).round(10)
    df['FACIL_Y'] = (df['FACIL_LODE'] + df['FACIL_LOMI'] / 60 + df['FACIL_LOSE'] / 3600).round(10)

    columns_to_drop = ['FACIL_LODE', 'FACIL_LOMI', 'FACIL_LOSE', 'FACIL_LADE',
                       'FACIL_LAMI', 'FACIL_LASE', 'FACIL_DTL_NM', 'FACIL_UNIT',
                       'FACIL_DTL_CODE', 'FACIL_GBN_CODE']

    df.drop(columns_to_drop, axis=1, inplace=True)

    return df


# 지정된 디렉토리에서 모든 .json 파일을 가져옵니다.
dir_path = "./shelter_json"
all_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.json')]

dfs = []
for file in all_files:
    full_path = os.path.join(dir_path, file)  # 여기서 전체 경로를 생성합니다.
    df = load_and_process_data(full_path)  # 전체 경로를 함수에 전달합니다.
    dfs.append(df)

# 모든 데이터프레임을 하나로 합칩니다.
merged_df = pd.concat(dfs, ignore_index=True)

merged_df.to_csv('./shelter.csv', encoding='utf-8-sig')

# 여기까지 진행하면 merged_df가 모든 JSON 파일의 데이터를 합친 데이터프레임이 됩니다.
