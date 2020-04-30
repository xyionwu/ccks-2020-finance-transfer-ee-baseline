import json
import pandas as pd

def check_num_type():
    lst = []
    in_file = open('train.json','r')
    for line in in_file:
        line = line.strip()
        line = json.loads(line)
        #print(line)
        ids = line['id']
        content = line['content']
        for k in line['events']:
            evn_type = k['type']
            lst.append(evn_type)
    lst = set(lst)
    print(lst)
    
def change_data():
    in_file = open('train.json','r')
    final_lst = []
    for line in in_file:
        org_lst = ['质押','股份股权转让','起诉','投资','高管减持']
        line = line.strip()
        line = json.loads(line)
        #print(line)
        ids = line['id']
        content = line['content']
        lst = []
        for k in line['events']:
            evn_type = k['type']
            lst.append(evn_type)
        #print(ids,content,lst)
        label_lst = []
        label_lst.append(ids)
        label_lst.append(content)
        for i in org_lst:
            if i in lst:
                label_lst.append(1)
            else:
                label_lst.append(0)
        #print(label_lst)
        final_lst.append(label_lst)
    return final_lst

def get_cls_df():
    final_lst = change_data()
    df = pd.DataFrame()
    df = df.append(final_lst,ignore_index=True)
    df.columns = ['id','content','zy','gfgqzr','qs','tz','ggjc']
    df.to_csv('CCKS-Bert-Multi-Label-Text-Classification/pybert/dataset/train_sample.csv',index=0)
    
if __name__ == '__main__':
    #check_num_type()
    #get_cls_data()
    get_cls_df()