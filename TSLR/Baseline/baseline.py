import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import make_pipeline
import time

# 加载数据
train_data_path = 'E:/Homework/学科资料/云计算/app/datasets/train-00000-of-00001.parquet'  # 替换为实际的路径
val_data_path = 'E:/Homework/学科资料/云计算/app/datasets/validation-00000-of-00001.parquet'  # 替换为实际的路径
test_data_path = 'E:/Homework/学科资料/云计算/app/datasets/test-00000-of-00001.parquet'  # 替换为实际的路径

train_df = pd.read_parquet(train_data_path)
val_df = pd.read_parquet(val_data_path)
test_df = pd.read_parquet(test_data_path)

# 数据预览
print("Training Data Preview:")
print(train_df.head())

# 合并句子
train_df['text'] = train_df['sentence1'] + ' ' + train_df['sentence2']
val_df['text'] = val_df['sentence1'] + ' ' + val_df['sentence2']
test_df['text'] = test_df['sentence1'] + ' ' + test_df['sentence2']

# 特征提取：使用TF-IDF向量化
tfidf_vectorizer = TfidfVectorizer(max_features=1000)

# 将数据分为训练集和验证集
X_train = train_df['text']
y_train = train_df['label']
X_val = val_df['text']
y_val = val_df['label']
X_test = test_df['text']
y_test = test_df['label']

# 创建一个pipeline，包含TF-IDF转换和逻辑回归模型
pipeline = make_pipeline(
    TfidfVectorizer(max_features=1000),
    LogisticRegression(max_iter=100)
)

# 记录训练开始时间
start_train_time = time.time()

# 训练模型
pipeline.fit(X_train, y_train)

# 记录训练结束时间
end_train_time = time.time()
train_time = end_train_time - start_train_time
print(f"Training Time: {train_time:.4f} seconds")

# 在验证集上进行预测
start_val_time = time.time()

val_predictions = pipeline.predict(X_val)
val_proba = pipeline.predict_proba(X_val)[:, 1]  # 获取正类的概率

# 记录验证结束时间
end_val_time = time.time()
val_time = end_val_time - start_val_time
print(f"Validation Time: {val_time:.4f} seconds")

# 评估验证集
print("Validation Classification Report:")
print(classification_report(y_val, val_predictions))

val_auc = roc_auc_score(y_val, val_proba)
print(f"Validation AUC: {val_auc}")

# 在测试集上进行预测
start_test_time = time.time()

test_predictions = pipeline.predict(X_test)
test_proba = pipeline.predict_proba(X_test)[:, 1]  # 获取正类的概率

# 记录测试结束时间
end_test_time = time.time()
test_time = end_test_time - start_test_time
print(f"Test Time: {test_time:.4f} seconds")

# 显示测试集的预测结果
print("Test Data Predictions:")
print(test_predictions[:5])

# 测试模型性能
test_auc = roc_auc_score(y_test, test_proba)
print(f"Test AUC: {test_auc}")
