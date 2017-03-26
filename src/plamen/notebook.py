from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import json
import re
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

dataset_path = '../../big_data/rb-suppliers-challange/receipts.csv'
texts_path = '../../big_data/rb-suppliers-challange/texts/'


def find_class_frequencies(dataset, group_col='currency_code'):
    codes = dataset.groupby(group_col).size()
    return codes


def load_dataset():
    dataset = pd.read_csv(dataset_path, index_col=['id'])
    dataset = dataset[~dataset.supplier_name.isnull()]
    dataset = dataset[~dataset.currency_code.isnull()]
    return dataset


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_json():
    dataset = load_dataset()
    file_names = [f.split(".")[0] for f in listdir(texts_path) if isfile(join(texts_path, f)) and f.endswith('.json')]
    ids = np.array(list(set([int(f) for f in file_names]).intersection(set(dataset.index.values))))
    texts = pd.Series(['' for i in ids], index=ids)
    for index in ids:
        json_data = open(texts_path + str(index) + '.json', encoding="utf8")
        data = json.load(json_data)
        try:
            texts[index] = clean_str(data[0]['textAnnotations'][0]['description'])
        except:
            texts[index] = ''
    return texts


def read_dataset_and_shuffle():
    dataset = load_dataset()
    print("Initial shape:", dataset.shape)
    print("Shape after filter:", dataset.shape)
    print("Columns names:")
    print(dataset.columns.values)

    dataset['texts'] = load_json()
    np.random.seed(1)
    shuffled = dataset.reindex(np.random.permutation(dataset.index))
    return shuffled


def classify_suppliers(dataset):
    test_slice = int(len(dataset) * (10 / 100))
    training_set = dataset[test_slice:]
    test_set = dataset[:test_slice]
    # classifier_benchmark = Pipeline([
    #     ('counts', CountVectorizer(max_features=2000000, min_df=2, ngram_range=(1, 3),stop_words='english')),
    #     ('tfidf', TfidfTransformer()),
    #     ('classification', LinearSVC(class_weight='balanced', random_state=1))
    # ])
    # classifier_nvb = Pipeline([
    #     ('counts', CountVectorizer(max_features=2000000, min_df=2, ngram_range=(1, 3), stop_words='english')),
    #     ('tfidf', TfidfTransformer()),
    #     ('classification',MultinomialNB())
    # ])
    classifier_mlp = Pipeline([
        ('counts', CountVectorizer(max_features=2000000, min_df=2, ngram_range=(1, 3), stop_words='english')),
        ('tfidf', TfidfTransformer()),
        ('classification', MLPClassifier())
    ])
    # classifier_benchmark.fit(training_set['texts'], training_set['supplier_name'])
    # classifier_nvb.fit(training_set['texts'], training_set['supplier_name'])
    s = pickle.dumps(classifier_mlp)

    classifier_mlp.fit(training_set['texts'], training_set['supplier_name'])
    print("Test set score {0}".format(classifier_mlp.score(test_set['texts'], test_set['supplier_name'])))
    # print("Test set score {0}".format(classifier_nn.score(test_set['texts'], test_set['supplier_name'])))
    # print("Test set score {0}".format(classifier_lda.score(test_set['texts'], test_set['supplier_name'])))
    print()


def main():
    dataset = read_dataset_and_shuffle()
    classify_suppliers(dataset)


if __name__ == '__main__':
    main()
