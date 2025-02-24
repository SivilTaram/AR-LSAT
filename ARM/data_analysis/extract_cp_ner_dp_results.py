import json
import os
import nltk
from tqdm import tqdm
import re
from tqdm import tqdm
import sys
from rule_pattern import RulePattern
from collections import Counter
RP = RulePattern()
basic_dir = "../../data/"
datap = os.path.join(basic_dir, 'AR_DevelopmentData.json')
outp = os.path.join(basic_dir, 'cp_ner_dp_results/AR_DevelopData_cp_ner_dp_results.json')
data = json.load(open(datap, 'r'))
def clean_doc(doc):
    # doc = ' '+doc
    # doc = doc.replace('—', ' — ')
    # doc = doc.replace('—', ' — ')
    doc = doc.replace('\u2014',' \u2014 ')
    return doc
all_passages = []
for passage in tqdm(data):
    # passages = exam['sections'][0]['passages']

    # for pidx,passage in enumerate(passages):
    doc = clean_doc(passage['passage'])#incase the first word is a number
    passage['passage'] = doc
    ques = passage['questions']
    sens = nltk.sent_tokenize(doc)

    sen_tokens, sen_ent_res, sen_dps = RP.get_cp_ner_results(sens)
    passage['sentences'] = sens
    passage['sentence_cp_results'] = []
    passage['sentence_ner_results'] = []
    passage['sentence_dp_results'] = []
    for idx in range(len(sens)):

        passage['sentence_cp_results'].append(sen_tokens[idx])#['hierplane_tree']['root'])
        passage['sentence_ner_results'].append(sen_ent_res[idx])
        passage['sentence_dp_results'].append(sen_dps)

    #analyze keywords in question and answer
    ques_text = [que['question'] for que in ques]
    ques_tokens, ques_ent_res, ques_dps = RP.get_cp_ner_results(ques_text)
    all_ques_kws = []
    all_opt_kws = []
    for idx in range(len(ques)):
        passage['questions'][idx]['question_cp_results'] =  ques_tokens[idx]#['hierplane_tree']['root']
        passage['questions'][idx]['question_ner_results'] = ques_ent_res[idx]
        passage['questions'][idx]['question_dp_results'] = ques_dps[idx]

        options = ques[idx]['options']
        # print(options)
        opt_tokens, opt_ent_res, opt_dps = RP.get_cp_ner_results(options)
        passage['questions'][idx]['option_cp_results'] = opt_tokens#[token['hierplane_tree']['root'] for token in opt_tokens]
        passage['questions'][idx]['option_ner_results'] = opt_ent_res
        passage['questions'][idx]['option_dp_results'] = opt_dps


    all_passages.append(passage)

with open(outp,'w',encoding='utf8') as outf:
    json.dump(all_passages,outf)





