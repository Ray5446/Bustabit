# Bustabit 玩家行為分析與流失預警系統
> **基於 RFM 模型與隨機森林演算法的數據驅動研究**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PowerBI](https://img.shields.io/badge/Visualization-Power%20BI-orange.svg)
![ML](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-green.svg)

## 📌 專案概述
本專案針對線上博弈平台 **Bustabit** 的 50,000 筆真實交易紀錄進行深度挖掘。旨在解決博弈產業中「高獲客成本」與「玩家易流失」的痛點，透過建立**主動式流失預警機制**，在玩家離開前精準識別風險，協助營運團隊優化 RTP（體感勝率）並制定留存策略。

## 📊 核心成果
* **流失捕捉率 (Recall):** <font color="red">**94%**</font> (精準識別出 137/145 名流失玩家)。
* **模型準確度 (Accuracy):** **84%**。
* **綜合評價 (F1-Score):** **0.89**。
* **數據規模:** 處理約 50,000 筆數據紀錄。

## 🛠 技術架構

### 1. 數據工程 (ETL)
* 使用 **Power Query (M 語言)** 與 **Python (Pandas)** 進行自動化數據清洗。
* **異常值處理：** 運用統計學方法識別並排除異常倍率數據，確保建模分析的信確度。

### 2. 玩家分群 (Segmentation)
* **RFM 模型：** 萃取最近遊玩日 (Recency)、頻率 (Frequency) 與投注金額 (Monetary)。
* **K-Means 演算法：** 透過手肘法 (Elbow Method) 決定最佳 K 值，將玩家劃分為：
    * **高價值玩家**：貢獻度高且活躍。
    * **保守型玩家**：下注謹慎但頻率穩定。
    * **一般玩家**：普通活躍度。
    * **沉寂玩家**：已出現明顯流失徵兆。

### 3. 預測建模 (Machine Learning)
* **演算法：** 隨機森林 (Random Forest)。
* **模型優化：** 針對類別不平衡問題，設定 `class_weight='balanced'`，極大化模型對流失行為的敏感度。

## 💡 商業洞察與建議
1.  **損耗點識別：** 透過分析發現玩家在連續虧損或體感勝率過低時的心理邊界，定義為關鍵損耗點。
2.  **差異化挽留：**
    * 針對「高價值」流失風險者，提供 VIP 專屬回饋。
    * 針對「一般」流失風險者，調整 **RTP (體感勝率)** 以提升遊戲延續感。

## 📂 檔案結構
```bash
├── Data/                # 原始數據集 (Bustabit.csv)
├── Notebooks/           # Python 分析與隨機森林建模腳本
├── Visuals/             # Power BI 交互式報表與視覺化圖表
├── Presentation/        # 專案說明 PPT 與成果總結
└── README.md            # 專案說明文件
