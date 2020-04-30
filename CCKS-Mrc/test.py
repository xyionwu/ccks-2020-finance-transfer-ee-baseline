from Io.data_loader import create_batch_iter
from preprocessing.data_processor import read_squad_data, convert_examples_to_features, read_qa_examples
from pytorch_pretrained_bert.tokenization import BertTokenizer
from predict.predict import main

if __name__ == "__main__":
    read_squad_data("data/squad_like_test.json", "data/",is_training=False)
    examples = read_qa_examples("data/", "test")
    main('data/')
