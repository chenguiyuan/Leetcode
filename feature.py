"""
Feature
"""

import numpy as np
import pandas as pd
import datetime
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold, RepeatedKFold
from sklearn.metrics import mean_squared_error

train = pd.read_csv("F:\\Kaggle\\Elo\\data\\train.csv")
test = pd.read_csv("F:\\Kaggle\\Elo\\data\\test.csv")
test_card_id = test[['card_id']]
historical_transactions = pd.read_csv("F:\\Kaggle\\Elo\\data\\historical_transactions.csv")
new_merchant_transactions = pd.read_csv("F:\\Kaggle\\Elo\\data\\new_merchant_transactions.csv")


# 异常值处理, 异常值2207
train['outliers'] = 0
train.loc[train['target'] < -30, 'outliers'] = 1
# print(train['outliers'].value_counts())

# for features in ['feature_1', 'feature_2', 'feature_3']:
#     order_label = train.groupby([features])['outliers'].mean()
#     train[features] = train[features].map(order_label)
#     test[features] = test[features].map(order_label)

# 天数
# 转换first_active_month为时间格式
train['first_active_month'] = pd.to_datetime(train['first_active_month'])
test['first_active_month'] = pd.to_datetime(test['first_active_month'])

train['days'] = (datetime.date(2018, 2, 1) - train['first_active_month'].dt.date).dt.days
feature_cols = ['feature_1', 'feature_2', 'feature_3']
for f in feature_cols:
    train['days_' + f] = train['days'] * train[f]
    train['days_' + f + '_ratio'] = train[f] / train['days']

test['days'] = (datetime.date(2018, 2, 1) - test['first_active_month'].dt.date).dt.days
feature_cols = ['feature_1', 'feature_2', 'feature_3']
for f in feature_cols:
    test['days_' + f] = test['days'] * test[f]
    test['days_' + f + '_ratio'] = test[f] / test['days']

# 缺失值处理
new_merchant_transactions['category_2'].fillna(1.0, inplace=True)
new_merchant_transactions['category_3'].fillna('A', inplace=True)
new_merchant_transactions['merchant_id'].fillna('M_ID_00a6ca8a8a', inplace=True)
new_merchant_transactions['installments'].replace(-1, np.nan, inplace=True )
new_merchant_transactions['purchase_amount'] = new_merchant_transactions['purchase_amount'].apply(lambda x: min(x, 0.8))

# 特征工程
new_merchant_transactions['authorized_flag'] = new_merchant_transactions['authorized_flag'].map({'Y': 1, 'N': 0})
new_merchant_transactions['category_1'] = new_merchant_transactions['category_1'].map({'Y': 1, 'N': 0})
new_merchant_transactions['category_3'] = new_merchant_transactions['category_3'].map({'A': 1, 'B': 2, 'C': 3})

new_merchant_transactions['purchase_date'] = pd.to_datetime(new_merchant_transactions['purchase_date'])
new_merchant_transactions['month'] = new_merchant_transactions['purchase_date'].dt.month
new_merchant_transactions['weekofyear'] = new_merchant_transactions['purchase_date'].dt.weekofyear
new_merchant_transactions['day'] = new_merchant_transactions['purchase_date'].dt.day
new_merchant_transactions['weekday'] = new_merchant_transactions['purchase_date'].dt.weekday
new_merchant_transactions['weekend'] = (new_merchant_transactions['purchase_date'].dt.weekday > 5).astype(int)
new_merchant_transactions['hour'] = new_merchant_transactions['purchase_date'].dt.hour
new_merchant_transactions['month_diff'] = ((datetime.datetime.today() - new_merchant_transactions['purchase_date']).dt.days) //30
new_merchant_transactions['month_diff'] += new_merchant_transactions['month_lag']

new_merchant_transactions['duration'] = new_merchant_transactions['purchase_amount'] * new_merchant_transactions['month_diff']
new_merchant_transactions['amount_month_ratio'] = new_merchant_transactions['purchase_amount'] / new_merchant_transactions['month_diff']
new_merchant_transactions['price'] = new_merchant_transactions['purchase_amount'] / new_merchant_transactions['installments']

for col in ['category_2', 'category_3']:
    new_merchant_transactions[col + '_mean'] = new_merchant_transactions['purchase_amount'].groupby(
        new_merchant_transactions[col]).agg('mean')
    new_merchant_transactions[col + '_max'] = new_merchant_transactions['purchase_amount'].groupby(
        new_merchant_transactions[col]).agg('max')
    new_merchant_transactions[col + '_min'] = new_merchant_transactions['purchase_amount'].groupby(
        new_merchant_transactions[col]).agg('min')
    new_merchant_transactions[col + '_sum'] = new_merchant_transactions['purchase_amount'].groupby(
        new_merchant_transactions[col]).agg('sum')


"""
自选特征
feature_sum
"""
for feature in ['feature_1', 'feature_2', 'feature_3']:
    new_merchant_transactions['feature_sum'] += new_merchant_transactions[feature]



# aggregate函数
def aggregate_historical_transactions(transactions, prefix):
    agg_function = {
        'purchase_amount': ['sum', 'max', 'min', 'mean', 'var', 'skew'],
        'installments': ['sum', 'max', 'mean', 'var', 'skew'],
        'purchase_date': ['max', 'min'],
        'month_lag': ['max', 'min', 'mean', 'var', 'skew'],
        'month_diff': ['max', 'min', 'mean', 'var', 'skew'],
        'weekend': ['sum', 'mean'],
        'weekday': ['sum', 'mean'],
        'authorized_flag': ['sum', 'mean'],
        'category_1': ['sum', 'mean', 'max', 'min'],
        'card_id': ['size', 'count'],
        'month': ['nunique', 'mean', 'min', 'max'],
        'hour': ['nunique', 'mean', 'min', 'max'],
        'weekofyear': ['nunique', 'mean', 'min', 'max'],
        'day': ['nunique', 'mean', 'min', 'max'],
        'subsector_id': ['nunique'],
        'merchant_category_id': ['nunique'],
        'price': ['sum', 'mean', 'max', 'min', 'var'],
        'duration': ['mean', 'min', 'max', 'var', 'skew'],
        'amount_month_ratio': ['mean', 'min', 'max', 'var', 'skew']
    }
    agg_transactions = transactions.groupby(['card_id']).agg(agg_function)
    agg_transactions.columns = [prefix + '_'.join(col).strip() for col in agg_transactions.columns.values]
    agg_transactions.reset_index(inplace=True)
    df = (transactions.groupby(['card_id']).size().reset_index(name='{}transactions_count'.format(prefix)))
    agg_transactions = pd.merge(df, agg_transactions, on='card_id', how='left')

    return agg_transactions

merge_new = aggregate_historical_transactions(new_merchant_transactions, prefix='new_')
train = pd.merge(train, merge_new, on='card_id', how='left')
test = pd.merge(test, merge_new, on='card_id', how='left')
train.reset_index(inplace=True)
test.reset_index(inplace=True)
train.to_csv("F:\\Kaggle\\Elo\\data\\train_merge.csv")
test.to_csv("F:\\Kaggle\\Elo\\data\\test_merge.csv")