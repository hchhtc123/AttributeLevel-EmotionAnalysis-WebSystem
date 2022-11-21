
# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import paddle
import random
import numpy as np
from seqeval.metrics.sequence_labeling import get_entities

def set_seed(seed):
    paddle.seed(seed)
    random.seed(seed)
    np.random.seed(seed)

def format_print(results):
    for result in results:
        aspect, opinion = result[0], set(result[1:])
        print(f"aspect: {aspect}, opinion: {opinion}\n")

def decoding(text, tag_seq):
    assert len(text) == len(tag_seq), f"text len: {len(text)}, tag_seq len: {len(tag_seq)}"

    puncs = list(",.?;!，。？；！")
    splits = [idx for idx in range(len(text)) if text[idx] in puncs]

    prev = 0
    sub_texts, sub_tag_seqs = [], []
    for i, split in enumerate(splits):
        sub_tag_seqs.append(tag_seq[prev:split])
        sub_texts.append(text[prev:split])
        prev = split
    sub_tag_seqs.append(tag_seq[prev:])
    sub_texts.append((text[prev:]))

    ents_list = []
    for sub_text, sub_tag_seq in zip(sub_texts, sub_tag_seqs):
        ents = get_entities(sub_tag_seq, suffix=False)
        ents_list.append((sub_text, ents))

    aps = []
    no_a_words = []
    for sub_tag_seq, ent_list in ents_list:
        sub_aps = []
        sub_no_a_words = []
        # print(ent_list)
        for ent in ent_list:
            ent_name, start, end = ent
            if ent_name == "Aspect":
                aspect = sub_tag_seq[start:end+1]
                sub_aps.append([aspect])
                if len(sub_no_a_words) > 0:
                    sub_aps[-1].extend(sub_no_a_words)
                    sub_no_a_words.clear()
            else:
                ent_name == "Opinion"
                opinion = sub_tag_seq[start:end + 1]
                if len(sub_aps) > 0:
                    sub_aps[-1].append(opinion)
                else:
                    sub_no_a_words.append(opinion)

        if sub_aps:
            aps.extend(sub_aps)
            if len(no_a_words) > 0:
                aps[-1].extend(no_a_words)
                no_a_words.clear()
        elif sub_no_a_words:
            if len(aps) > 0:
                aps[-1].extend(sub_no_a_words)
            else:
                no_a_words.extend(sub_no_a_words)

    if no_a_words:
        no_a_words.insert(0, "None")
        aps.append(no_a_words)

    return aps 
    
def is_aspect_first(text, aspect, opinion_word):
    return text.find(aspect) <= text.find(opinion_word)

def concate_aspect_and_opinion(text, aspect, opinion_words):
    aspect_text = ""
    for opinion_word in opinion_words:
        if is_aspect_first(text, aspect, opinion_word):
            aspect_text += aspect+opinion_word+"，"
        else:
            aspect_text += opinion_word+aspect+"，"
    aspect_text = aspect_text[:-1]

    return aspect_text

def format_print(results):
    for result in results:
        aspect, opinions, sentiment = result["aspect"], result["opinions"], result["sentiment"]
        print(f"aspect: {aspect}, opinions: {opinions}, sentiment: {sentiment}")
    print()
