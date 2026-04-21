import pandas as pd
import numpy as np

df = pd.read_csv(r'C:\python projects\bustabit\bustabit.csv')

df['PlayDate'] = pd.to_datetime(df['PlayDate'])

df['CashedOut'] = df['CashedOut'].fillna(0)

df['Profit'] = df.apply(lambda x: -x['Bet'] if pd.isna(x['Profit']) else x['Profit'], axis=1)

df['is_win'] = (df['CashedOut'] > 0).astype(int)

user_start = df.groupby('Username')['PlayDate'].min().reset_index()
user_start.columns = ['Username', 'JoinDate']

df = df.merge(user_start, on='Username')
df['RelativeDay'] = (df['PlayDate'] - df['JoinDate']).dt.days

df_X = df[df['RelativeDay'] <= 21]

df_y = df[(df['RelativeDay'] > 21) & (df['RelativeDay'] <= 35)]

features = df_X.groupby('Username').agg({
    'RelativeDay': lambda x: 21 - x.max(), 
    'GameID': 'count',
    'Bet': 'sum',
    'Profit': 'sum',
    'is_win': 'mean',
    'CashedOut': 'mean'
}).reset_index()

features.columns = ['Username', 'Recency', 'Frequency', 'Monetary', 'Net_Profit', 'Win_Rate', 'Avg_Multiplier']

features['R_Rank'] = pd.qcut(features['Recency'].rank(method='first'), 5, labels=[5,4,3,2,1]).astype(int)
features['F_Rank'] = pd.qcut(features['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
features['M_Rank'] = pd.qcut(features['Monetary'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)

active_users_future = df_y['Username'].unique()

features['Churn'] = features['Username'].apply(lambda x: 0 if x in active_users_future else 1)

max_date = df['PlayDate'].max()
features = features[features['Username'].isin(user_start[user_start['JoinDate'] <= max_date - pd.Timedelta(days=35)]['Username'])]

features.to_csv(r'C:\python projects\bustabit\processed_features.csv', index=False, encoding='utf-8-sig')
