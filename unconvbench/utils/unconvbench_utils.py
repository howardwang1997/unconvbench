import json
import os
from os.path import dirname as up

import pandas as pd
from pymatgen.core import Structure
from sklearn.model_selection import KFold

from .constant import DATASETS_LEN

CODE_PATH = up(up(os.path.abspath(__file__)))


def _get_list_name(name, length, index):
    r_len = len(str(length))
    all_names = [name + '-' + str(i+1).rjust(r_len, '0') for i in index]
    return all_names


def make_splits(name, length, n_folds=5, random_seed=42):
    kf = KFold(n_folds, random_state=random_seed, shuffle=True)
    index = list(range(length))
    dataset_split = {}
    for i, (train_index, test_index) in enumerate(kf.split(index)):
        f = {'train': _get_list_name(name, length, train_index), 'test': _get_list_name(name, length, test_index)}
        dataset_split.update({f'fold_{i}': f})
    dataset = {name: dataset_split}
    return dataset


def make_validation(n_folds=5, random_seed=42, save=False):
    validation = {}
    for k, v in DATASETS_LEN.items():
        validation.update(make_splits(k, v, n_folds, random_seed))
    metadata = {'n_split': n_folds, 'random_state': random_seed, 'shuffle': True}

    final = {'metadata': metadata, 'splits': validation}
    if save:
        with open(os.path.join(CODE_PATH, 'utils', 'metadata_validation.json'), 'w+') as f:
            json.dump(final, f)
    return final


def load_dataset(dataset, name):
    data = [Structure.from_dict(d[0]) for d in dataset['data']]
    labels = [d[1] for d in dataset['data']]
    length = len(data)
    index = list(range(length))

    all_names = _get_list_name(name, length, index)
    pd_idx = pd.Series(all_names, name='id')
    inputs = pd.Series(data, name=dataset['columns'][0], index=pd_idx)
    outputs = pd.Series(labels, name=dataset['columns'][1], index=pd_idx)

    return inputs, outputs
