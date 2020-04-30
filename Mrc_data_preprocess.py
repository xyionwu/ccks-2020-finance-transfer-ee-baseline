import json
import pandas as pd
import random

def get_word_error_data():
    out_file = open('word_error_data.txt','w')
    in_file = open('train.json','r')
    final_lst = []
    id_lst = []
    for line in in_file:
        line = line.strip()
        line = json.loads(line)
        ids = line['id']
        content = line['content']
        for k in line['events']:
            evn_type = k['type']
            for i in k['mentions']:
                word = i['word']
                start_span = i['span'][0]
                end_span = i['span'][1]
                span_word = content[start_span:end_span]
                span = str(start_span)+','+str(end_span)
                x = content.find(word)
                if span_word != word:
                    id_lst.append(ids)
                    lst=[ids,word]
                    final_lst.append(lst)
                    out_file.write(ids+'\t'+'错因：span抽取出来的元素与word不一致'+'\t'+word+'\t'+span+'\t'+content+'\n')                   
                    #final_lst = set(final_lst)
    #print(len(final_lst))
    #print(final_lst)
    return id_lst

def get_span_error_data():
    id_lst = get_word_error_data()
    #print(len(id_lst))
    out_file = open('span_error_data.txt','w')
    in_file = open('train.json','r')
    final_lst = []
    for line in in_file:
        line = line.strip()
        line = json.loads(line)
        ids = line['id']
        content = line['content']
        for k in line['events']:
            evn_type = k['type']
            for i in k['mentions']:
                word = i['word']
                len_content = len(content)
                start_span = i['span'][0]
                end_span = i['span'][1]
                span = str(start_span)+','+str(end_span)
                if start_span<0:
                    id_lst.append(ids)
                    lst=[ids,span]
                    final_lst.append(lst)
                    out_file.write(ids+'\t'+'错因：起始位置<0'+'\t'+span+'\t'+word+'\t'+content+'\n')
                elif start_span>end_span:
                    id_lst.append(ids)
                    lst=[ids,span]
                    final_lst.append(lst)                    
                    out_file.write(ids+'\t'+'错因：起始位置>终止位置'+'\t'+span+'\t'+word+'\t'+content+'\n')
                elif start_span>len_content:
                    id_lst.append(ids)
                    lst=[ids,span]
                    final_lst.append(lst)                    
                    out_file.write(ids+'\t'+'错因：起始位置>文本长度'+'\t'+span+'\t'+word+'\t'+content+'\n')
                elif end_span>len_content:
                    id_lst.append(ids)
                    lst=[ids,span]
                    final_lst.append(lst)                    
                    out_file.write(ids+'\t'+'错因：终止位置>文本长度'+'\t'+span+'\t'+word+'\t'+content+'\n')
                    #final_lst = set(final_lst)
    #print(len(final_lst))
    #print(final_lst)
    #print(len(id_lst))
    #print(id_lst)
    id_lst = set(id_lst)
    #print(len(id_lst))
    #print(id_lst)
    return id_lst

def change_data():
    error_id_list = get_span_error_data()
    print(len(error_id_list))
    print(error_id_list)
    in_file = open('train.json','r')
    final_lst = []
    for line in in_file:
        line = line.strip()
        line = json.loads(line)
        ids = str(line['id'])
        if ids not in error_id_list:
            content = line['content']
            for k in line['events']:
                evn_type = k['type']
                for i in k['mentions']:
                    n = str(random.randint(0, 7))
                    ids = ids+'_'+n
                    lst = []
                    word = i['word']
                    word = word.replace('）',')')
                    word = word.replace('（','(')
                    word = word.replace('，',',')
                    word = word.replace('：',':')
                    start_span = i['span'][0]
                    end_span = i['span'][1]
                    #if start_span<0:
                    #    print(ids,start_span)
                    role = i['role']
                    all_lst = [ids,content,evn_type,word,start_span,role,end_span]
                    final_lst.append(all_lst)
    return final_lst

def get_df():
    final_lst = change_data()
    df = pd.DataFrame()
    df = df.append(final_lst,ignore_index=True)
    df.columns = ['id','content','type','word','start_span','role']
    df.to_csv('mrc_middle_data.csv',index=0)
    return df
        
        
def get_torch_mrc_all_data():
    final_lst = change_data()
    out_file = open('CCKS-Mrc/data/squad-like_all_data.json','w',encoding = 'utf-8')
    lst = []
    dic1 = {}
    dic2 = {}
    for i in range(len(final_lst)):
        tmp_con = {}
        tmp_ans = {}
        tmp_pos = {}
        tmp_con['context'] = final_lst[i][1]
        tmp_pos['answer_start'] = int(final_lst[i][4])
        tmp_pos['answer_end'] = int(final_lst[i][6])
        tmp_pos['text'] = final_lst[i][3]
        tmp_pos['answer_type'] = "long-answer"
        tmp_ans['answers'] = [tmp_pos]
        tmp_con['qas'] = [tmp_ans]
        qus = final_lst[i][2]
        role = final_lst[i][5]
        con_qus = '事件类型为'+qus+'的'+role+'是什么？'
        tmp_ans['question'] = con_qus
        tmp_ans['id'] = final_lst[i][0]
        lst.append(tmp_con)
    dic1['title'] = '小样本金融元素抽取'
    dic1['paragraphs'] = lst
    dic2['data'] = [dic1]
    dic2['version'] = '1.1'
    data = json.dumps(dic2,ensure_ascii=False,indent=0)
    print(len(data))
    out_file.write(data)
    
if __name__ == '__main__':
    #get_word_error_data()
    #get_span_error_data()
    get_torch_mrc_all_data()