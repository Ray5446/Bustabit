import pandas as pd
import numpy as np

# 讀取資料
df = pd.read_csv(r'C:\python projects\bustabit\bustabit.csv')

# 1. 時間轉換 (一定要先做，才能計算 Recency)
df['PlayDate'] = pd.to_datetime(df['PlayDate'])

# 2. 處理 CashedOut 的 NA 值 (NA 代表玩家沒領到錢就爆了，倍數設為 0)
df['CashedOut'] = df['CashedOut'].fillna(0)

# 3. 處理 Profit (如果 NA 則 Profit = -Bet)
df['Profit'] = df.apply(lambda x: -x['Bet'] if pd.isna(x['Profit']) else x['Profit'], axis=1)

# 4. 建立「是否獲勝」標籤 (用於後續計算勝率)
df['is_win'] = (df['CashedOut'] > 0).astype(int)

# 找出每個玩家的加入日期
user_start = df.groupby('Username')['PlayDate'].min().reset_index()
user_start.columns = ['Username', 'JoinDate']

# 合併回原表並計算「相對天數」
df = df.merge(user_start, on='Username')
df['RelativeDay'] = (df['PlayDate'] - df['JoinDate']).dt.days

# 切分資料
# X_data: 用來算 RFM 和分群的基礎
df_X = df[df['RelativeDay'] <= 21]

# y_data: 用來判斷是否流失 (第22~35天沒出現就是流失)
df_y = df[(df['RelativeDay'] > 21) & (df['RelativeDay'] <= 35)]

# 修改特徵計算邏輯
features = df_X.groupby('Username').agg({
    # 改成用 21 減去 玩家最後一次下注是在第幾天
    'RelativeDay': lambda x: 21 - x.max(), 
    'GameID': 'count',
    'Bet': 'sum',
    'Profit': 'sum',
    'is_win': 'mean',
    'CashedOut': 'mean'
}).reset_index()

# 重新命名欄位
features.columns = ['Username', 'Recency', 'Frequency', 'Monetary', 'Net_Profit', 'Win_Rate', 'Avg_Multiplier']

# 處理 R_Rank, F_Rank, M_Rank (為了分群)
features['R_Rank'] = pd.qcut(features['Recency'].rank(method='first'), 5, labels=[5,4,3,2,1]).astype(int)
features['F_Rank'] = pd.qcut(features['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
features['M_Rank'] = pd.qcut(features['Monetary'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)

# 找出在預測窗(22~35天)有出現過的玩家
active_users_future = df_y['Username'].unique()

# 標記：如果玩家沒出現在未來窗口，Churn = 1
features['Churn'] = features['Username'].apply(lambda x: 0 if x in active_users_future else 1)

# 過濾掉「剛加入還沒滿 35 天」的玩家，避免誤判
# (假設你的資料最後一天是 max_date)
max_date = df['PlayDate'].max()
features = features[features['Username'].isin(user_start[user_start['JoinDate'] <= max_date - pd.Timedelta(days=35)]['Username'])]

features.to_csv(r'C:\python projects\bustabit\processed_features.csv', index=False, encoding='utf-8-sig')