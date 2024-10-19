# my_spark.py
# spark-submit --master spark://hadoop.Master:7077 ./my_spark.py 
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator

import time

# 创建 SparkSession
spark = SparkSession.builder.appName("WiC_TextClassification").getOrCreate()

# 加载训练、验证和测试集
train_data_path = "/dataset/wic/train-00000-of-00001.parquet"  # 替换为实际的训练集路径
val_data_path = "/dataset/wic/validation-00000-of-00001.parquet"      # 替换为实际的验证集路径
test_data_path = "/dataset/wic/test-00000-of-00001.parquet"  # 替换为实际的测试集路径

# 模型保存方法
model_path = "/model/wic-model" 

train_df = spark.read.parquet(train_data_path)
val_df = spark.read.parquet(val_data_path)
test_df = spark.read.parquet(test_data_path)

# 预览数据
print("Training Data Preview:")
train_df.show(5)

# 合并两个句子形成一个新的文本列
train_df = train_df.withColumn("text", concat_ws(" ", train_df.sentence1, train_df.sentence2))
val_df = val_df.withColumn("text", concat_ws(" ", val_df.sentence1, val_df.sentence2))
test_df = test_df.withColumn("text", concat_ws(" ", test_df.sentence1, test_df.sentence2))

# 分词
tokenizer = Tokenizer(inputCol="text", outputCol="words")

# 计算词频特征
hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=1000)

# 计算 IDF 特征
idf = IDF(inputCol="rawFeatures", outputCol="features")

# 标签编码
label_indexer = StringIndexer(inputCol="label", outputCol="indexedLabel")

# 逻辑回归模型
lr = LogisticRegression(featuresCol="features", labelCol="indexedLabel", maxIter=100)

# 创建一个管道，包含数据处理和模型训练步骤
pipeline = Pipeline(stages=[tokenizer, hashingTF, idf, label_indexer, lr])

# 训练模型
model = pipeline.fit(train_df)

# 保存模型
model.write().overwrite().save(model_path)

# 在验证集上进行预测
start_time = time.time()

val_predictions = model.transform(val_df)
val_predictions.select("idx", "sentence1", "sentence2", "label", "prediction").show(5)

# 评估模型性能
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="indexedLabel")
auc = evaluator.evaluate(val_predictions)
print(f"Validation AUC: {auc}")

end_time = time.time()
print(f"Validation Run Time: {end_time - start_time} s")

# 在验证集上进行预测
start_time = time.time()
# 对测试集进行预测
test_predictions = model.transform(test_df)

# 显示测试集的预测结果
print("Test Data Predictions:")
test_predictions.select("idx", "sentence1", "sentence2", "label", "prediction").show(5)

# 测试模型性能
auc_test = evaluator.evaluate(test_predictions)
print(f"Test AUC: {auc_test}")
end_time = time.time()
print(f"Validation Run Time: {end_time - start_time} s")

# 停止 SparkSession
spark.stop()
