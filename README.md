# Bustabit 玩家行為與流失率分析
> **基於 RFM 模型與隨機森林演算法的數據研究**

![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-2ecc71?style=flat&logo=scikit-learn&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=power-bi&logoColor=black)

## 📌 專案概述
本專案針對線上博弈平台 **Bustabit** 的 50,000 筆下注紀錄進行深度挖掘。旨在解決博弈產業中「玩家易流失」的痛點，透過建立**流失預警模型**，在玩家離開前識別風險，協助營運團隊優化並制定留存策略。


## 🛠 技術架構

### 1. 數據工程 
* 使用 **Python (Pandas)** 進行數據清洗。
* **Power Query：** 運用M語言進行數據轉換，確保建模分析的準確度。

### 2. 玩家分群 
* **RFM 模型：** 萃取最近遊玩日 (Recency)、下注頻率 (Frequency) 與投注總額 (Monetary)。
* **K-Means 演算法：** 透過手肘法決定最佳 K 值，將玩家劃分為：
    * **高價值玩家**：貢獻度高且活躍。
    * **保守型玩家**：下注謹慎但頻率穩定。
    * **一般玩家**：普通活躍度。
    * **沉寂玩家**：已出現明顯流失徵兆。

### 3. 預測建模 
* **演算法：** Random Forest。
* **流失捕捉率 :** <font color="red">**94%**</font>。
* **模型準確度 :** **84%**。
* **綜合評價 :** **0.89**。

## 💡 商業洞察與建議
1.  **損耗點識別：** 透過分析發現玩家在結束倍率或沉寂天數上升時的心理邊界，定義為關鍵損耗點。
2.  **挽留策略：**
    * 針對星期日，舉辦周末特別活動。
    * 針對沉寂玩家，在連續虧損後適當發放補償券。
