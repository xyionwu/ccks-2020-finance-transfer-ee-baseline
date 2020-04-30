import json
import pandas as pd
import random


def change_data():
    in_file = open('dataset/train.json','r')
    final_lst = []
    for line in in_file:
        line = line.strip()
        line = json.loads(line)
        ids = str(line['id'])
        content = line['content']
        for k in line['events']:
            evn_type = k['type']
            role_lst = []
            for i in k['mentions']:
                n = str(random.randint(0, 7))
                ids = ids+'_'+n
                lst = []
                word = i['word']
                start_span = i['span'][0]
                end_span = i['span'][1]
                role = i['role']
                role_lst.append(role)
                all_lst = [ids,content,evn_type,word,start_span,role,end_span]
                final_lst.append(all_lst)
            if evn_type=='质押':
                role_all = ['trigger','sub-org','sub-per','obj-org','obj-per','collateral','date','money','number','proportion']
            elif evn_type=='股份股权转让':
                role_all = ['trigger','sub-org','sub-per','obj-org','obj-per','collateral','date','money','number','proportion','Target-company']
            elif evn_type=='起诉':
                role_all = ['trigger','sub-org','sub-per','obj-org','obj-per','date']
            elif evn_type=='投资':
                role_all = ['trigger','sub','obj','money','date']
            elif evn_type=='减持':
                role_all = ['trigger','sub','title','date','share-per','share-org','org']
            for rol in role_all:  
                if rol not in role_lst:
                    n = str(random.randint(0, 7))
                    ids = ids+'_'+n
                    lst = []
                    word = ''
                    start_span = int(0)
                    end_span = int(0)
                    role = rol
                    all_lst = [ids,content,evn_type,word,start_span,role,end_span]
                    final_lst.append(all_lst)

                        
    return final_lst

def get_df():
    final_lst = change_data()
    df = pd.DataFrame()
    df = df.append(final_lst,ignore_index=True)
    df.columns = ['id','content','type','word','start_span','role']
    #df.to_csv('mrc_middle_data.csv',index=0)
    return df
        
        
def get_torch_mrc_all_train_data():
    final_lst = change_data()
    out_file = open('CCKS-Mrc/data/squad-like_all_train_data.json','w')
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
        text = final_lst[i][3]
        tmp_pos['text'] = text
        if text=='':
            tmp_pos['answer_type'] = "no-answer"
        else:
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
    out_file.write(data)
    print('Mrc模型的train集转换完成!')

def get_mrc_test_data():
    print('Mrc模型的test集转换中...')
    cls_out = pd.read_csv('CCKS-Cls/test_output/cls_out.csv')
    test_data = pd.read_csv('CCKS-Cls/pybert/dataset/test.csv')
    all_cls_test_df = test_data.merge(cls_out, on='id')
    out_file = open('CCKS-Mrc/data/squad_like_test.json','w')
    lst = []
    dic1 = {}
    dic2 = {}
    for index,row in all_cls_test_df.iterrows():
        ids,content=row["id"],row["content"]
        zy,gfgqzr,qs,tz,ggjc = row['zy'],row['gfgqzr'],row['qs'],row['tz'],row['ggjc'],
        #print(ids,content,zy,gfgqzr,qs,tz,ggjc)
        if zy==1:
            ctype = '质押'
            role_zy = ['trigger','sub-org','sub-per','obj-org','obj-per','collateral','date','money','number','proportion']
            for i in role_zy:
                n = str(random.randint(0, 7))
                ids = str(ids)+'_'+n
                tmp_con = {}
                tmp_ans = {}
                tmp_pos = {}
                tmp_con['context'] = content
                tmp_pos['answer_start'] = int(0)
                tmp_pos['answer_end'] = int(0)
                tmp_pos['text'] = ''
                tmp_pos['answer_type'] = ''
                tmp_ans['answers'] = [tmp_pos]
                tmp_con['qas'] = [tmp_ans]
                qus = ctype
                role = i
                con_qus = '事件类型为'+qus+'的'+role+'是什么？'
                tmp_ans['question'] = con_qus
                tmp_ans['id'] = ids
                lst.append(tmp_con)
        if gfgqzr==1:
            ctype = '股份股权转让'
            role_gfgqzr = ['trigger','sub-org','sub-per','obj-org','obj-per','collateral','date','money','number','proportion','Target-company']
            for i in role_gfgqzr:
                n = str(random.randint(0, 7))
                ids = str(ids)+'_'+n
                tmp_con = {}
                tmp_ans = {}
                tmp_pos = {}
                tmp_con['context'] = content
                tmp_pos['answer_start'] = int(0)
                tmp_pos['answer_end'] = int(0)
                tmp_pos['text'] = ''
                tmp_pos['answer_type'] = ''
                tmp_ans['answers'] = [tmp_pos]
                tmp_con['qas'] = [tmp_ans]
                qus = ctype
                role = i
                con_qus = '事件类型为'+qus+'的'+role+'是什么？'
                tmp_ans['question'] = con_qus
                tmp_ans['id'] = ids
                lst.append(tmp_con)
        if qs==1:
            ctype = '起诉'
            role_qs = ['trigger','sub-org','sub-per','obj-org','obj-per','date']
            for i in role_qs:
                n = str(random.randint(0, 7))
                ids = str(ids)+'_'+n
                tmp_con = {}
                tmp_ans = {}
                tmp_pos = {}
                tmp_con['context'] = content
                tmp_pos['answer_start'] = int(0)
                tmp_pos['answer_end'] = int(0)
                tmp_pos['text'] = ''
                tmp_pos['answer_type'] = ''
                tmp_ans['answers'] = [tmp_pos]
                tmp_con['qas'] = [tmp_ans]
                qus = ctype
                role = i
                con_qus = '事件类型为'+qus+'的'+role+'是什么？'
                tmp_ans['question'] = con_qus
                tmp_ans['id'] = ids
                lst.append(tmp_con)
        if tz==1:
            ctype = '投资'
            role_tz = ['trigger','sub','obj','money','date']
            for i in role_tz:
                n = str(random.randint(0, 7))
                ids = str(ids)+'_'+n
                tmp_con = {}
                tmp_ans = {}
                tmp_pos = {}
                tmp_con['context'] = content
                tmp_pos['answer_start'] = int(0)
                tmp_pos['answer_end'] = int(0)
                tmp_pos['text'] = ''
                tmp_pos['answer_type'] = ''
                tmp_ans['answers'] = [tmp_pos]
                tmp_con['qas'] = [tmp_ans]
                qus = ctype
                role = i
                con_qus = '事件类型为'+qus+'的'+role+'是什么？'
                tmp_ans['question'] = con_qus
                tmp_ans['id'] = ids
                lst.append(tmp_con)
        if ggjc==1:
            ctype = '减持'
            role_ggjc = ['trigger','sub','title','date','share-per','share-org','org']
            for i in role_ggjc:
                n = str(random.randint(0, 7))
                ids = str(ids)+'_'+n
                tmp_con = {}
                tmp_ans = {}
                tmp_pos = {}
                tmp_con['context'] = content
                tmp_pos['answer_start'] = int(0)
                tmp_pos['answer_end'] = int(0)
                tmp_pos['text'] = ''
                tmp_pos['answer_type'] = ''
                tmp_ans['answers'] = [tmp_pos]
                tmp_con['qas'] = [tmp_ans]
                qus = ctype
                role = i
                con_qus = '事件类型为'+qus+'的'+role+'是什么？'
                tmp_ans['question'] = con_qus
                tmp_ans['id'] = ids
                lst.append(tmp_con)
        if zy==0 and gfgqzr==0 and qs==0 and tz==0 and ggjc==0:
            ids = str(ids)
            #print(ids)
            tmp_con = {}
            tmp_ans = {}
            tmp_pos = {}
            tmp_con['context'] = content
            tmp_pos['answer_start'] = int(0)
            tmp_pos['answer_end'] = int(0)
            tmp_pos['text'] = ''
            tmp_pos['answer_type'] = ''
            tmp_ans['answers'] = [tmp_pos]
            tmp_con['qas'] = [tmp_ans]
            qus = ''
            role = ''
            con_qus = '事件类型为'+qus+'的'+role+'是什么？'
            tmp_ans['question'] = con_qus
            tmp_ans['id'] = ids
            lst.append(tmp_con)

    dic1['title'] = '小样本金融元素抽取'
    dic1['paragraphs'] = lst
    dic2['data'] = [dic1]
    dic2['version'] = '1.1'
    data = json.dumps(dic2,ensure_ascii=False,indent=0)
    out_file.write(data)
    print('Mrc模型的test集转换完成!')    
if __name__ == '__main__':
    get_torch_mrc_all_train_data()
    get_mrc_test_data()
