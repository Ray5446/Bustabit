import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. 載入資料
df = pd.read_csv(r'C:\python projects\bustabit\processed_features_with_clusters.csv')

# 2. 準備特徵 (X) 與 標籤 (y)
# 我們移除 Username (ID) 和 Churn (答案)，保留其他數值特徵
X = df.drop(['Username', 'Churn'], axis=1)
y = df['Churn']

# 3. 切分資料集 (80% 訓練模型, 20% 測試準確度)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 建立隨機森林模型
# class_weight='balanced' 很重要，因為流失玩家通常佔少數，這能平衡模型判斷力
rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
rf_model.fit(X_train, y_train)

# 5. 進行預測並查看報告
y_pred = rf_model.predict(X_test)
print("--- 模型評估報告 ---")
print(classification_report(y_test, y_pred))

# 6. 產出每個人的「流失機率」 (這對 Power BI 最有用)
# 我們預測整張表 X 的機率，並取第二欄 (機率為 1，即流失的機率)
df['Churn_Probability'] = rf_model.predict_proba(X)[:, 1]

# 7. 匯出最終結果
df.to_csv(r'C:\python projects\bustabit\prediction_results.csv', index=False, encoding='utf-8-sig')
print("\n預測完成！請查看 final_prediction_results.csv")

#1. 混淆矩陣到底在看什麼？
#classification_report 給你的是最終得分（分數），而 confusion_matrix 給你的是**「犯錯的細節」**。

#它會把結果拆解成四個象限：

#True Positive (TP): 成功抓到要流失的人（英雄）。

#True Negative (TN): 正確判斷留下來的人（穩健）。

#False Positive (FP): 「誤報」，人家明明沒要走，你卻說他要流失（浪費行銷成本）。

#False Negative (FN): 「漏抓」，人家要走了你卻沒發現（最痛的損失）。

#我透過混淆矩陣發現誤報（FP）有 50 人，漏抓（FN）有 10 人。假設挽回一個人的成本是 100 元，但失去一個人的價值是 1000 元，我能算出這個模型幫公司省下了多少錢。

#加入from matplotlib.colors import ListedColormap
