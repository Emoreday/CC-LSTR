# runMyModel.py
# spark-submit --master spark://hadoop.Master:7077 runMyModel.py

from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws
from pyspark.ml import PipelineModel
import threading

app = FastAPI()

# 创建 SparkSession
spark = SparkSession.builder.appName("WiC_TextPrediction").getOrCreate()

# 加载训练好的模型
model_path = "/model/wic-model"
model = PipelineModel.load(model_path)

class TextPair(BaseModel):
    sentence1: str
    sentence2: str

def predict_association(sentence1: str, sentence2: str) -> str:
    input_data = spark.createDataFrame([(sentence1, sentence2)], ["sentence1", "sentence2"])
    input_data = input_data.withColumn("text", concat_ws(" ", input_data.sentence1, input_data.sentence2))
    prediction = model.transform(input_data)
    result = prediction.select("prediction").collect()[0]
    return "Related" if result["prediction"] == 1.0 else "Not Related"

@app.post("/predict")
def predict(text_pair: TextPair):
    result = predict_association(text_pair.sentence1, text_pair.sentence2)
    return {"sentence1": text_pair.sentence1, "sentence2": text_pair.sentence2, "prediction": result}

# 运行 FastAPI
def run():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7001)

# 启动线程运行 FastAPI
thread = threading.Thread(target=run)
thread.start()

# 在此处可以添加其他 Spark 任务
