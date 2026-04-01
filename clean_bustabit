import pandas as pd
import numpy as np

# 1. 讀取資料
path = r'C:\python projects\bustabit\bustabit.csv'
df = pd.read_csv(path)

# (1) 移除沒有名字的無效紀錄
df_clean = df.dropna(subset=['Username'])
df_clean['Username'] = df_clean['Username'].astype(str)

# (2) 處理數值欄位的空值 
# 如果 Profit 是 NA，代表輸錢，利潤 = 負的Bet
df_clean['Profit'] = df_clean['Profit'].fillna(-df_clean['Bet'])

# 如果 CashedOut 或 Bonus 是 NA，填 0
df_clean['CashedOut'] = df_clean['CashedOut'].fillna(0)
df_clean['Bonus'] = df_clean['Bonus'].fillna(0)

# (C) 時間格式轉換 (方便 Power BI 建立時間軸)
df_clean['PlayDate'] = pd.to_datetime(df_clean['PlayDate'])

# 4. 儲存
df_clean.to_csv(r'C:\python projects\bustabit\clean_bustabit.csv', index=False, encoding='utf-8-sig')


print("清洗完成！事實表與維度表已同步輸出。")