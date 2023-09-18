import pandas as pd


adm_code = pd.read_excel('./adm_code.xls', header=1)
adm_code[['시도코드', '시군구코드', '읍면동코드']] = adm_code[['시도코드', '시군구코드', '읍면동코드']].astype(str)

sido_code = adm_code['시도코드'].unique()
sido_name = adm_code['시도명칭'].unique()
sido_df = pd.DataFrame({'병합_명칭': sido_name, '병합_코드': sido_code})
gungu_code = adm_code['시도코드'] + adm_code['시군구코드']
gungu_code = gungu_code.unique()
gungu_name = adm_code['시도명칭'] + " " + adm_code['시군구명칭']
gungu_name = gungu_name.unique()
gungu_df = pd.DataFrame({'병합_명칭': gungu_name, '병합_코드': gungu_code})
myeondong_code = adm_code['시도코드'] + adm_code['시군구코드'] + adm_code['읍면동코드']
myeondong_name = adm_code['시도명칭'] + " " + adm_code['시군구명칭'] + " " + adm_code['읍면동명칭']
myeondong_df = pd.DataFrame({'병합_명칭': myeondong_name, '병합_코드': myeondong_code})

total_df = pd.concat([sido_df, gungu_df, myeondong_df], axis=0, ignore_index=True)
total_df.to_excel('total_code.xlsx')

