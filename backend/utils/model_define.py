import paddle

class SkepForTokenClassification(paddle.nn.Layer):
    def __init__(self, skep, num_classes=2, dropout=None):
        super(SkepForTokenClassification, self).__init__()
        self.num_classes = num_classes
        self.skep = skep
        self.dropout = paddle.nn.Dropout(dropout if dropout is not None else self.skep.config["hidden_dropout_prob"])
        self.classifier = paddle.nn.Linear(self.skep.config["hidden_size"], num_classes)

    def forward(self, input_ids, token_type_ids=None, position_ids=None, attention_mask=None):
        sequence_output, _ = self.skep(input_ids, token_type_ids=token_type_ids, position_ids=position_ids, attention_mask=attention_mask)

        sequence_output = self.dropout(sequence_output)
        logits = self.classifier(sequence_output)
        return logits

class SkepForSequenceClassification(paddle.nn.Layer):
    def __init__(self, skep, num_classes=2, dropout=None):
        super(SkepForSequenceClassification, self).__init__()
        self.num_classes = num_classes
        self.skep = skep
        self.dropout = paddle.nn.Dropout(dropout if dropout is not None else self.skep.config["hidden_dropout_prob"])
        self.classifier = paddle.nn.Linear(self.skep.config["hidden_size"], num_classes)

    def forward(self, input_ids, token_type_ids=None, position_ids=None, attention_mask=None):
        _, pooled_output = self.skep(input_ids, token_type_ids=token_type_ids, position_ids=position_ids, attention_mask=attention_mask)

        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)
        return logits