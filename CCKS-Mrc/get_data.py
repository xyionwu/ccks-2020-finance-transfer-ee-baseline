from preprocessing.data_processor import read_squad_data

if __name__ == "__main__":
    read_squad_data("data/squad-like_all_train_data.json", "data/",is_training=True)


