# ---------- Train -------------------
log_path = "output/logs"
plot_path = "output/images/loss_acc.png"
data_dir = "data/"
output_dir = "output/checkpoint"
VOCAB_FILE = "/home/jeramy/下载/Pretrain-Model-Pytorch/chinese_wwm_ex_bert/vocab.txt"
bert_model = "/home/jeramy/下载/Pretrain-Model-Pytorch/chinese_wwm_ex_bert"
doc_stride = 128
#max_query_length = 32
#max_seq_length = 256
max_query_length = 128
max_seq_length = 512
do_lower_case = True
train_batch_size = 5
eval_batch_size = 5
learning_rate = 2e-5
num_train_epochs = 3
warmup_proportion = 0.1
no_cuda = False
local_rank = -1
seed = 42
gradient_accumulation_steps = 2
fp16 = False
loss_scale = 0.

answer_type = {"no-answer": 0, "long-answer": 1}

# ------------ Predict -----------------
predict_batch_size = 16
n_best_size = 1
max_answer_length = 256
verbose_logging = 1
#version_2_with_negative = True
version_2_with_negative = False
null_score_diff_threshold = 0
