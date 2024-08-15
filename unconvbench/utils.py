import hashlib
import json
import os
from os.path import dirname as up

import numpy as np
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
        with open(os.path.join(CODE_PATH, 'datasets', 'metadata_validation.json'), 'w+') as f:
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


def immutify_dictionary(d):
    """Create a frozenset-esque deterministic, unique representation of
    a nested dict, from matbench.


    Args:
        d (dict): The dictionary to be immutified. Key are always strings.
            Values can be arrays of various numpy or pandas types, strings,
            numpy primitives, python native numbers, or dictionaries with
            the same format.

    Returns:
        (dict): A sorted, deterministic, unique representation of the
            dictionary.
    """
    d_new = {}
    for k, v in d.items():
        if isinstance(v, (np.ndarray, pd.Series)):
            d_new[k] = tuple(v.tolist())
        elif isinstance(v, list):
            d_new[k] = tuple(v)
        elif isinstance(v, dict):
            d_new[k] = immutify_dictionary(v)
        else:
            # convert numpy types to native
            if hasattr(v, "dtype"):
                d_new[k] = v.item()
            else:
                d_new[k] = v
    # dictionaries are ordered in python 3.6+
    return dict(sorted(d_new.items(), key=lambda item: item[0]))


def hash_dictionary(d):
    """Hash a dictionary that can be immutified with immutify_dictionary, from matbench.

    Order of the keys does not matter, as dictionary becomes deterministically
    immutified. Dictionary can be nested.

    Args:
        d (dict): The dictionary to hash.

    Returns:
        (str): base16 encoded hash of the dictionary.
    """
    d_hashable = immutify_dictionary(d)
    s_hashable = json.dumps(d_hashable).encode("utf-8")
    m = hashlib.sha256(s_hashable).hexdigest()
    return m
