import json
import numpy as np
import random
import os

from src import data_helper
from collections import Counter
from termcolor import cprint
import plac


def split_data_train_val_test(m=10, datapath="data/wiki_all.json", outfolder="data/"):
    cprint(f"split {datapath} with {m} unseen relations")
    data, _ = data_helper.load_data(datapath)
    label = list(i['edgeSet'][0]['kbID'] for i in data)
    pid, count = np.unique(label, return_counts=True)
    pid2cnt = dict(zip(pid, count))
    # randomly select n unseen labels for testing
    test_relation = random.sample(list(pid2cnt), m)
    train_data_, test_data = data_helper.split_wiki_data(data, test_relation)

    # randomly select n unseen labels for validation
    val_relation = random.sample(list(pid2cnt), m)
    train_data, val_data = data_helper.split_wiki_data(train_data_, val_relation)


    cprint(f"train {len(train_data)}, val {len(val_data)}, test {len(test_data)}")

    output = os.path.join(outfolder, f"m{m}")
    if not os.path.exists(output):
        os.mkdir(output)

    with open(os.path.join(output, "wiki_train.json"), "w") as f:
        json.dump(train_data, f)

    with open(os.path.join(output, "wiki_val.json"), "w") as f:
        json.dump(val_data, f)

    with open(os.path.join(output, "wiki_test.json"), "w") as f:
        json.dump(test_data, f)


if __name__ == '__main__':
    plac.call(split_data_train_val_test)

