import pandas as pd
import numpy as np

# 1. 讀取洗乾淨的事實表
path = r"C:\python projects\bustabit\clean_bustabit.csv"
df = pd.read_csv(path)

# 2. 取得不重複玩家清單
clean_usernames = df['Username'].unique()
num_users = len(clean_usernames)

# 3. 定義國家清單與對應權重
countries = [
    'Taiwan', 'Japan', 'South Korea', 'Hong Kong',    # 東亞 (主要市場)
    'Malaysia', 'Thailand', 'Vietnam', 'Philippines', # 東南亞 (成長市場)
    'USA', 'Canada', 'Brazil',                        # 美洲
    'UK', 'Germany', 'France'                         # 歐洲
]

# 設定權重 (總和需為 1)
weights = [
    0.25, 0.15, 0.10, 0.05,  # 東亞合計 55%
    0.15, 0.05, 0.05, 0.05,  # 東南亞合計 30%
    0.05, 0.02, 0.01,        # 美洲合計 8%
    0.03, 0.02, 0.02         # 歐洲合計 7%
]

# 4. 建立維度表 (將註冊日期鎖定在 2016-11 之前)
users_dim = pd.DataFrame({
    'Username': clean_usernames,
    'Country': np.random.choice(countries, num_users, p=weights),
    'Device': np.random.choice(['iOS', 'Android', 'PC'], num_users, p=[0.4, 0.45, 0.15]),
    'User_Tier': np.random.choice(['Bronze', 'Silver', 'Gold', 'VIP'], num_users, p=[0.7, 0.2, 0.08, 0.02]),
    
    # 修改：基準日為 2016-01-01，隨機增加 0~304 天，確保日期在 2016/10/31 之前
    'Reg_Date': pd.to_datetime('2016-01-01') + pd.to_timedelta(np.random.randint(0, 305, num_users), unit='D')
})

# 5. 儲存
users_dim.to_csv(r'C:\python projects\bustabit\users_dim.csv', index=False, encoding='utf-8-sig')

# 驗證輸出
print(f"清洗與維度建模完成！")
print(f"總玩家數：{num_users}")
print("-" * 30)
print(f"維度表前五筆：\n{users_dim.head()}")
print("-" * 30)
print(f"註冊日期範圍：{users_dim['Reg_Date'].min().date()} 至 {users_dim['Reg_Date'].max().date()}")