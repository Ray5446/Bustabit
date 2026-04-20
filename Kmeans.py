import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

features = pd.read_csv(r'H:\python projects\bustabit\processed_features.csv')

cluster_features = features[['R_Rank', 'F_Rank', 'M_Rank']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(cluster_features)

sse = []
k_range = range(1, 11) 

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_features)
    sse.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(k_range, sse, 'bx-', markersize=8)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('SSE (Inertia)')
plt.title('Elbow Method For Optimal k')
plt.xticks(k_range)
plt.grid(True)
plt.show()


kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
features['Cluster'] = kmeans.fit_predict(scaled_features)

score = silhouette_score(scaled_features, features['Cluster'])

print(f"\n--- 分群驗證報告 ---")
print(f"樣本總數: {len(features)}")
print(f"分群輪廓分數 (k=4): {score:.4f}")

features.to_csv(r'C:\python projects\bustabit\clusters.csv', index=False, encoding='utf-8-sig')
