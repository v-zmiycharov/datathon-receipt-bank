import os
import numpy as np
import pandas as pd
from scipy.io import mmwrite
from sklearn.cluster import DBSCAN
from scipy.io import mmread
from fuzzywuzzy import fuzz
from time import gmtime, strftime
from collections import defaultdict

dataset_path = '../../big_data/rb-suppliers-challange/receipts.csv'

OUTPUT_DIR = "/home/phristov/datathon/datathon-receipt-bank/src/plamen/output/"


def find_class_frequencies(dataset, group_col='currency_code'):
    codes = dataset.groupby(group_col).size()
    return codes


def read_dataset_and_shuffle():
    dataset = pd.read_csv(dataset_path, index_col=['id'])
    dataset = dataset[~dataset.supplier_name.isnull()]
    dataset = dataset[~dataset.currency_code.isnull()]
    print(len(dataset))
    # shuffled = dataset.reindex(np.random.permutation(dataset.index))
    return dataset


def cleanse_folder():
    dataset = read_dataset_and_shuffle()
    names = list(map(str, dataset.index.values))
    for root, dirs, files in os.walk(
            '/home/phristov/datathon/datathon-receipt-bank/big_data/rb-suppliers-challange/texts/'):
        for name in files:
            path = os.path.join(root, name)
            if os.path.isfile(path):
                extracted_name = name[:name.index('.')]
                if extracted_name not in names:
                    os.remove(path)


def compute_similarity(s1, s2):
    return 1.0 - (0.01 * max(
        fuzz.ratio(s1, s2),
        fuzz.token_sort_ratio(s1, s2),
        fuzz.token_set_ratio(s1, s2)))


def create_stats_matrix():
    shuffled = read_dataset_and_shuffle()
    suppliers = shuffled.supplier_name
    X = np.zeros((len(suppliers), len(suppliers)))
    for i in range(len(suppliers)):
        if i > 0 and i % 10 == 0:
            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": Processed %d/%d rows of data" % (i, X.shape[0]))
        for j in range(len(suppliers)):
            if X[i, j] == 0.0:
                X[i, j] = compute_similarity(suppliers.values[i].lower(), suppliers.values[j].lower())
                X[j, i] = X[i, j]
    mmwrite(os.path.join(OUTPUT_DIR, "stats_suppliers.mtx"), X)


def cluster_suppliers():
    X = mmread(os.path.join(OUTPUT_DIR, "stats_suppliers.mtx"))
    clust = DBSCAN(eps=0.1, min_samples=2, metric="precomputed")
    clust.fit(X)

    # print cluster report
    stitles = []
    shuffled = read_dataset_and_shuffle()
    suppliers = shuffled.supplier_name
    for line in suppliers:
        stitles.append(line.strip().split("\t")[0])

    preds = clust.labels_
    clabels = np.unique(preds)
    for i in range(clabels.shape[0]):
        if clabels[i] < 0:
            continue
        cmem_ids = np.where(preds == clabels[i])[0]
        cmembers = defaultdict(set)
        for cmem_id in cmem_ids:
            cmembers[i].add(stitles[cmem_id])
        print("Cluster#%d: %s" % (i, ", ".join(cmembers[i])))


def main():
    pass
    # create_stats_matrix()
    # cluster_suppliers()
    # read_dataset_and_shuffle()
    # cleanse_folder()

if __name__ == '__main__':
    main()
