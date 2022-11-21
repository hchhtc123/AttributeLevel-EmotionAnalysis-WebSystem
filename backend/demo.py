"""
    demo演示程序：
    加载训练好的模型进行属性级情感分析
    单文本情感分析：针对输入的语句进行单文本情感分析
    批量文本情感分析：Pandas读取Excel文件内容后进行批量情感分析
"""

# 导入所需依赖
import pandas as pd
import paddle
from paddlenlp.transformers import SkepTokenizer, SkepModel
from utils.utils import decoding, concate_aspect_and_opinion, format_print
from utils import data_ext, data_cls
from utils.model_define import SkepForTokenClassification, SkepForSequenceClassification

# 单条文本情感分析预测函数
def predict(input_text, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label, max_seq_len=512):
    ext_model.eval()
    cls_model.eval()

    # processing input text
    encoded_inputs = tokenizer(list(input_text), is_split_into_words=True, max_seq_len=max_seq_len,)
    input_ids = paddle.to_tensor([encoded_inputs["input_ids"]])
    token_type_ids = paddle.to_tensor([encoded_inputs["token_type_ids"]])

    # extract aspect and opinion words
    logits = ext_model(input_ids, token_type_ids=token_type_ids)
    predictions = logits.argmax(axis=2).numpy()[0]
    tag_seq = [ext_id2label[idx] for idx in predictions][1:-1]
    aps = decoding(input_text, tag_seq)

    # predict sentiment for aspect with cls_model
    results = []
    for ap in aps:
        aspect = ap[0]
        opinion_words = list(set(ap[1:]))
        aspect_text = concate_aspect_and_opinion(input_text, aspect, opinion_words)
        
        encoded_inputs = tokenizer(aspect_text, text_pair=input_text, max_seq_len=max_seq_len, return_length=True)
        input_ids = paddle.to_tensor([encoded_inputs["input_ids"]])
        token_type_ids = paddle.to_tensor([encoded_inputs["token_type_ids"]])

        logits = cls_model(input_ids, token_type_ids=token_type_ids)
        prediction = logits.argmax(axis=1).numpy()[0]

        result = {"aspect": aspect, "opinions": str(opinion_words), "sentiment": cls_id2label[prediction]}
        results.append(result)

    # print results
    format_print(results)

    # 返回预测结果
    return results

# 批量情感分析预测函数
def batchPredict(data, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label, max_seq_len=512):

    ext_model.eval()
    cls_model.eval()

    analysisResults = []

    # 针对批量文本逐条处理
    for input_text in data:
        # processing input text
        encoded_inputs = tokenizer(list(input_text), is_split_into_words=True, max_seq_len=max_seq_len,)
        input_ids = paddle.to_tensor([encoded_inputs["input_ids"]])
        token_type_ids = paddle.to_tensor([encoded_inputs["token_type_ids"]])

        # extract aspect and opinion words
        logits = ext_model(input_ids, token_type_ids=token_type_ids)
        predictions = logits.argmax(axis=2).numpy()[0]
        tag_seq = [ext_id2label[idx] for idx in predictions][1:-1]
        aps = decoding(input_text, tag_seq)

        # predict sentiment for aspect with cls_model
        results = []
        for ap in aps:
            aspect = ap[0]
            opinion_words = list(set(ap[1:]))
            aspect_text = concate_aspect_and_opinion(input_text, aspect, opinion_words)
            
            encoded_inputs = tokenizer(aspect_text, text_pair=input_text, max_seq_len=max_seq_len, return_length=True)
            input_ids = paddle.to_tensor([encoded_inputs["input_ids"]])
            token_type_ids = paddle.to_tensor([encoded_inputs["token_type_ids"]])

            logits = cls_model(input_ids, token_type_ids=token_type_ids)
            prediction = logits.argmax(axis=1).numpy()[0]

            result = {"属性": aspect, "观点": opinion_words, "情感倾向": cls_id2label[prediction]}
            results.append(result)
        singleResult = {"text": input_text, "result": str(results)}
        analysisResults.append(singleResult)

    # 返回预测结果 list形式
    return analysisResults

if __name__== "__main__" :
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

    # 单条文本情感分析
    max_seq_len = 512
    input_text = "环境装修不错，也很干净，前台服务非常好"
    predict(input_text, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label,  max_seq_len=max_seq_len)

    input_text = "蛋糕味道不错，很好吃，店家很耐心，服务也很好，很棒"
    predict(input_text, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label,  max_seq_len=max_seq_len)

    # 读取Excel文件内容进行批量情感分析
    df = pd.read_excel('./resource/测试数据.xlsx', index_col=None)
    # 读取Excel中列名为"text"或"文本"的数据，若无该列名则默认读取第一列数据
    if 'text' in df.columns:
        contents = df['text']
    elif '文本' in df.columns:
        contents = df['文本']
    else: contents = df[df.columns[0]]

    # 批量文本情感分析
    batchResult = batchPredict(contents, ext_model, cls_model, tokenizer, ext_id2label, cls_id2label,  max_seq_len=512)
    print(batchResult)






