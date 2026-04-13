import pandas as pd
from sklearn.cluster import KMeans

# 1. 讀取資料
df = pd.read_csv(r'C:\python projects\bustabit\Dim_users.csv') 

# 2. RFM 等級分類 (1-5 分)
df['R_Rank'] = pd.qcut(df['Recency'], 5, labels=[5, 4, 3, 2, 1])
df['F_Rank'] = pd.qcut(df['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
df['M_Rank'] = pd.qcut(df['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# 3. 準備模型輸入資料
X = df[['R_Rank', 'F_Rank', 'M_Rank']]

# 4. 執行 K-Means
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X)

# 5. 查看結果
print("--- 前 5 筆分群結果 ---")
print(df[['Username', 'R_Rank', 'F_Rank', 'M_Rank', 'Cluster']].head())

# 6. 分析每一群的特徵 (修正關鍵：先將欄位轉為 float)
print("\n--- 各分群平均等級 (1-5 分) ---")
# 指定需要計算的欄位
target_cols = ['R_Rank', 'F_Rank', 'M_Rank']
# 先轉型，再 groupby 算平均
cluster_summary = df.copy()
cluster_summary[target_cols] = cluster_summary[target_cols].astype(float)
analysis = cluster_summary.groupby('Cluster')[target_cols].mean()
print(analysis)

# 7. 儲存結果 (加上 utf-8-sig 確保中文與 Excel 相容)
df.to_csv(r'C:\python projects\bustabit\KMeans_Results.csv', index=False, encoding='utf-8-sig')
print("\n分群成功！結果已存入 KMeans_Results.csv")