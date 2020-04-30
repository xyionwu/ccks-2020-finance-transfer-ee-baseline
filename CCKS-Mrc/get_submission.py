import pandas as pd
import json
import re

def get_sample_lst():
    mrc_pre = open('output/checkpoint/predictions.json',encoding='utf-8')
    out_data = json.load(mrc_pre)
    mrc_test = open('data/test.json', "r", encoding="utf-8")
    lst = []
    for data in mrc_test:
        data = data.strip()
        data = json.loads(data)
        qid = str(data['qid'])
        context = data['context']
        question = data["question"]
        data['type'] = re.findall("为(.*?)\的", question)[0]
        data['role'] = re.findall("的(.*?)\是", question)[0]
        for key,value in out_data.items():
            if key ==qid:
                value = value.replace(' ','')
                #print(qid,value)
                if value !='':
                    data['word']=value
                    span_start = context.find(value)
                    span_end = span_start+len(value)
                    if "_" in qid:
                        qids = str(qid.split("_")[0])
                    else:
                        qids = qid
                    sample = {"id":qids,"events":[{"type":data['type'],
                                    "mentions":[{"word":value,"span":[span_start,span_end],"role":data['role']
                                        }]}]}
                    lst.append(sample)
    return lst

def merge_type_lst():
    sub_data = open('submission.json','w',encoding='utf-8')
    sample_lst = get_sample_lst()
    official_test_df = open('../dataset/test.json','r',encoding='utf-8')
    merge_lst = []
    for line in official_test_df:
        line = line.strip()
        line = json.loads(line)
        ids = line['id']
        sam_lst = []
        for k in sample_lst:
            if ids ==k['id']:
                sample=k.copy()
                sample.pop("id")
                sample = sample['events'][0]
                sam_lst.append(sample)
        sam_dic = {"id":ids,"events":sam_lst}
        merge_lst.append(sam_dic)
    #print(merge_lst)
    for i in merge_lst:
        ids=i['id']
        evnets=i['events']
        sub_dic={}
        info_dic = {}
        for d in evnets:
            if d['type'] not in info_dic:
                info_dic[d['type']] = d['mentions']
                list1 = info_dic[d['type']]
            else:
                info_dic[d['type']] = info_dic[d['type']]+d['mentions']
        sub_dic['id']=ids
        t_list = []
        for key,value in info_dic.items():
            dic1={}
            dic1['type']=key
            dic1['mentions']=value
            t_list.append(dic1)
        sub_dic['events']=t_list
        #print(sub_dic)
        json.dump(sub_dic, sub_data, ensure_ascii=False)
        sub_data.write('\n')
        
if __name__ == '__main__':
    merge_type_lst()
