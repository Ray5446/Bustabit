import pandas as pd

# 1. 讀取洗乾淨的事實表
path = r"C:\python projects\bustabit\clean_bustabit.csv"
df = pd.read_csv(path)

# 確保日期格式正確
df['PlayDate'] = pd.to_datetime(df['PlayDate'])

# 2. 聚合計算：以 Username 為中心，算出 R, F, C
# R (Recency): 最後一次玩的日期
# F (Frequency): 玩的總次數 (Id 的計數)
# C (Monetary/Profit): 總利潤 (Profit 的總和)
dim_users = df.groupby('Username').agg(
    Recency_Date=('PlayDate', 'max'),
    Frequency=('Id', 'count'),
    Monetary=('Profit', 'sum')
).reset_index()

# 3. 將最後日期轉換為「距離今天幾天」的數字 (Recency)
# 我們用資料集裡面的最後一天當作基準點
ref_date = dim_users['Recency_Date'].max()
dim_users['Recency'] = (ref_date - dim_users['Recency_Date']).dt.days

# 4. 只保留你要的欄位：Username, Recency, Frequency, Total_Profit (C)
result = dim_users[['Username', 'Recency', 'Frequency', 'Monetary']]

# 如果要存成 CSV 給後續使用：
result.to_csv(r'C:\python projects\bustabit\Dim_users.csv', index=False, encoding='utf-8-sig')


