import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

# 1. 讀取事實表
# 使用 r 前綴確保路徑中的反斜槓不會被誤認為轉義字元
file_path = r'C:\python projects\bustabit\事實表.csv'
df_raw = pd.read_csv(file_path)

# 2. 處理日期與相對天數 (修正報錯的核心部分)
def convert_to_datetime(series):
    # 先處理中文 AM/PM
    temp_series = series.astype(str).str.replace('上午', 'AM').str.replace('下午', 'PM')
    # 使用 pd.to_datetime 進行向量化轉換，errors='coerce' 會把無法轉換的變成空值
    return pd.to_datetime(temp_series, format='%Y/%m/%d %p %I:%M:%S', errors='coerce')

df_raw['PlayDate'] = convert_to_datetime(df_raw['PlayDate'])

# 移除日期轉換失敗的無效行，確保剩下的都是 datetime64 型態
df_raw = df_raw.dropna(subset=['PlayDate'])

# 計算每個玩家的第一天
df_raw['FirstDate'] = df_raw.groupby('Username')['PlayDate'].transform('min')

# 計算相對天數 (RelativeDay) - 修正後的寫法
# 這裡先轉為 date 再相減，並取 .days 屬性
df_raw['RelativeDay'] = (df_raw['PlayDate'].dt.date - df_raw['FirstDate'].dt.date).apply(lambda x: x.days)

# 3. 提取全站玩家特徵 (前 21 天行為)
df_21 = df_raw[df_raw['RelativeDay'] <= 21].copy()
all_players = df_21.groupby('Username').agg({
    'RelativeDay': lambda x: 21 - x.max(),  # Recency
    'GameID': 'count',                      # Frequency
    'Bet': 'sum',                           # Monetary
    'Profit': 'sum',                        # Net_Profit
    'CashedOut': 'mean'                     # Avg_Multiplier
}).reset_index()

# 計算勝率
win_rate = df_21.groupby('Username')['Profit'].apply(lambda x: (x > 0).mean()).reset_index()
all_players = all_players.merge(win_rate, on='Username')
all_players.columns = ['Username', 'Recency', 'Frequency', 'Monetary', 'Net_Profit', 'Avg_Multiplier', 'Win_Rate']

# 4. 計算 R, F, M Ranks (1-5 分)
for col, rank_name in [('Recency', 'R_Rank'), ('Frequency', 'F_Rank'), ('Monetary', 'M_Rank')]:
    if col == 'Recency':
        all_players[rank_name] = pd.qcut(all_players[col].rank(method='first'), 5, labels=[5, 4, 3, 2, 1]).astype(int)
    else:
        all_players[rank_name] = pd.qcut(all_players[col].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)

# 5. 載入訓練標籤並訓練模型
# 讀取原本的 1000 人標籤表
train_df = pd.read_csv(r'C:\python projects\bustabit\processed_features_with_clusters.csv')
all_players_master = all_players.merge(train_df[['Username', 'Churn']], on='Username', how='left')

# 訓練模型
features_list = ['Recency', 'Frequency', 'Monetary', 'Net_Profit', 'Win_Rate', 'Avg_Multiplier', 'R_Rank', 'F_Rank', 'M_Rank']
all_players_master[features_list] = all_players_master[features_list].fillna(0) # 填補缺失值

known = all_players_master.dropna(subset=['Churn'])

# 訓練隨機森林
rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf.fit(known[features_list], known['Churn'])

# 訓練 K-Means
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans.fit(known[['R_Rank', 'F_Rank', 'M_Rank']])

# 6. 預測全站玩家
all_players_master['Cluster'] = kmeans.predict(all_players_master[['R_Rank', 'F_Rank', 'M_Rank']])
all_players_master['Churn_Probability'] = rf.predict_proba(all_players_master[features_list])[:, 1]

# 7. 匯出最後的「玩家維度總表」
output_path = r'C:\python projects\bustabit\all_players_master_table.csv'
all_players_master.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"處理成功！檔案已儲存至: {output_path}")
print(f"總玩家數: {len(all_players_master)}")