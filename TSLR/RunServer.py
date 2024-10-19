# runMyModel.py
# spark-submit --master spark://hadoop.Master:7077 runMyModel.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat_ws
from pyspark.ml import PipelineModel
import threading

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（也可以指定具体的域名列表）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法（GET, POST, OPTIONS等）
    allow_headers=["*"],  # 允许所有请求头
)

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

