## 数据及预训练模型准备
(1)将比赛数据集train.json和test.json放置在dataset文件中
(2)将预训练模型放置在pretrained_model中，
     对于分类模型，可在CCKS-Bert-Multi-Label-Text-Classification\pybert\configs\basic_config.py进行路径修改
	 对于阅读理解模型，可在CCKS-Mrc\config\args.py进行路径修改
(3)可在以下地址自行下载pytorch pretrained_model:https://github.com/ymcui/Chinese-BERT-wwm
(4)注意预训练模型里面文件名与代码config中设置的一致

## 先训练Cls分类模型
(1)数据预处理:python Cls_data_preprocess.py
(2)数据切分: python run_bert.py --do_data to preprocess data
(3)模型训练：python run_bert.py --do_train --save_best
(4)模型推断: python run_bert.py --do_test

## 后训练Mrc阅读理解模型
(1)数据预处理:python Mrc_data_preprocess.py
(2)数据切分: python get_data.py
(3)模型训练：python train_start.py
(4)模型推断: python test.py

## 生成比赛提交文件
(1)python get_submission.py

## 注意：
(1)请严格按照顺序运行命令
(2)请按照requirements.txt配置环境
(2)可自行更换预训练模型，或者在config中更改如epoch等参数进行调参优化
(3)本代码只提供基础的思路，欢迎在此基础上继续做模型改进和优化

