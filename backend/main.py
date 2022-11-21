"""
    基于FastAPI的属性级情感分析后端模块
    先加载观点抽取和情感分析模型预热后再启动后端接口服务
"""

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time
import paddle
from paddlenlp.transformers import SkepTokenizer, SkepModel
from utils import data_ext, data_cls
from utils.model_define import SkepForTokenClassification, SkepForSequenceClassification
from demo import predict, batchPredict

# 模型预热
print("加载训练好的模型参数！")
label_ext_path = "./label_ext.dict"
label_cls_path = "./label_cls.dict"

# 加载PaddleNLP开源的基于全量数据训练好的评论观点抽取模型和属性级情感分类模型
ext_model_path = "./model/best_ext.pdparams"
cls_model_path = "./model/best_cls.pdparams"

# load dict
model_name = "skep_ernie_1.0_large_ch"
ext_label2id, ext_id2label = data_ext.load_dict(label_ext_path)
cls_label2id, cls_id2label = data_cls.load_dict(label_cls_path)
tokenizer = SkepTokenizer.from_pretrained(model_name)
print("label dict loaded.")

# load ext model   观点抽取模型
ext_state_dict = paddle.load(ext_model_path)
ext_skep = SkepModel.from_pretrained(model_name)
ext_model = SkepForTokenClassification(ext_skep, num_classes=len(ext_label2id))    
ext_model.load_dict(ext_state_dict)
print("extraction model loaded.")

# load cls model   属性级情感分析模型
cls_state_dict = paddle.load(cls_model_path)
cls_skep = SkepModel.from_pretrained(model_name)
cls_model = SkepForSequenceClassification(cls_skep, num_classes=len(cls_label2id))    
cls_model.load_dict(cls_state_dict)
print("classification model loaded.")

# 模型预热，属性级情感分析
max_seq_len = 512
input_text = "环境装修不错，也很干净，前台服务非常好"
predict(input_text, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label,  max_seq_len=max_seq_len)

# 创建一个 FastAPI「实例」，名字为app
app = FastAPI()

# 设置允许跨域请求，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义请求体数据类型：text  用户输入的要进行属性级情感分析的文本
class Document(BaseModel):
    text: str

# 定义路径操作装饰器：POST方法 + API接口路径
# 单文本情感分析接口
@app.post("/v1/singleEmotionAnalysis/", status_code=200)
# 定义路径操作函数，当接口被访问将调用该函数
async def SingleEmotionAnalysis(document: Document):
    try:
        # 获取用户输入的要进行属性级情感分析的文本内容
        input_text = document.text
        # 调用加载好的模型进行属性级情感分析
        singleAnalysisResult = predict(input_text, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label,  max_seq_len=512)
        # 接口结果返回
        results = {"message": "success", "inputText": document.text, "singleAnalysisResult": singleAnalysisResult}
        return results
    # 异常处理
    except Exception as e:
        print("异常信息：", e)
        raise HTTPException(status_code=500, detail=str("请求失败，服务器端发生异常！异常信息提示：" + str(e)))

# 批量文本情感分析接口
# 定义路径操作装饰器：POST方法 + API接口路径
@app.post("/v1/batchEmotionAnalysis/", status_code=200)
# 定义路径操作函数，当接口被访问将调用该函数
async def BatchEmotionAnalysis(file: UploadFile):
    # 读取上传的文件
    fileBytes = file.file.read()
    fileName = file.filename
    # 判断上传文件类型
    fileType = fileName.split(".")[-1]
    if fileType != "xls" and fileType != "xlsx":
        raise HTTPException(status_code=406, detail=str("请求失败，上传文件格式不正确！请上传Excel文件！"))
    try:
        # 将添加时间标记重命名避免重复
        now_time = int(time.mktime(time.localtime(time.time())))
        filePath = "./resource/" + str(now_time) + "_" + fileName
        # 将用户上传的文件保存到本地
        fout = open(filePath, 'wb')
        fout.write(fileBytes)
        fout.close()
        # 读取Excel文件内容进行批量情感分析
        df = pd.read_excel(filePath, index_col=None)
        # 读取Excel中列名为"text"或"文本"的数据，若无该列名则默认读取第一列数据
        if 'text' in df.columns:
            contents = df['text']
        elif '文本' in df.columns:
            contents = df['文本']
        else: contents = df[df.columns[0]]
        # 批量文本情感分析
        batchAnalysisResults = batchPredict(contents, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label,  max_seq_len=512)
        # 接口结果返回
        results = {"message": "success", "batchAnalysisResults": batchAnalysisResults}
        return results
    # 异常处理
    except Exception as e:
        print("异常信息：", e)
        raise HTTPException(status_code=500, detail=str("请求失败，服务器端发生异常！异常信息提示：" + str(e)))

# 启动创建的实例app，设置启动ip和端口号
uvicorn.run(app, host="127.0.0.1", port=8000)
