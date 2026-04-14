from sklearn.cluster import KMeans
import pandas as pd

# 1. 讀取特徵表
features = pd.read_csv(r'C:\python projects\bustabit\processed_features.csv')

# 2. 選擇分群用的特徵 (建議用 Rank，因為數值已經標準化在 1-5 之間)
cluster_features = features[['R_Rank', 'F_Rank', 'M_Rank']]

# 3. 執行 K-Means (設定分為 4 群)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
features['Cluster'] = kmeans.fit_predict(cluster_features)

# 4. 查看每一群的 RFM 平均值，用來定義群體名稱
cluster_summary = features.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'Win_Rate': 'mean',
    'Churn': 'mean',
    'Username': 'count'
}).rename(columns={'Username': 'Player_Count'})

# 5. 匯出成 CSV
features.to_csv(r'C:\python projects\bustabit\clusters.csv', index=False, encoding='utf-8-sig')

print("\n分群完成！已匯出至 processed_features_with_clusters.csv")