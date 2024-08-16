import json
import os
from os.path import dirname as up

from monty.json import MSONable
import torch
import numpy as np
import pandas as pd
from torch.nn import L1Loss, MSELoss

from .constant import DATASETS_LEN, DATASETS_RESULTS
from .utils import load_dataset

CODE_PATH = up(up(os.path.abspath(__file__)))


class DotDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Task:
    def __init__(self, name, **kwargs):
        self.benchmark_name = 'unconvbench-1.0.1'
        self.dataset_name = name
        self.metadata = {
            'input_type': 'structure',
            'n_samples': DATASETS_LEN[name],
            'nun_entries': DATASETS_LEN[name],
            'task_type': 'regression',
            'file_type': 'json.gz',
            'columns': {'structure': 'Structure.', 'target': 'Target.'},
            'mad': 1,
            'target': 'target',
            'unit': 'TBA',
            'bibtex_refs': 'TBA',
            'description': 'TBA',
            'reference': 'TBA',
            'url': 'TBA',
            'hash': 'TBA'
        }
        self.metadata = DotDict(self.metadata)
        self.folds_map = {0: 'fold_0', 1: 'fold_1', 2: 'fold_2', 3: 'fold_3', 4: 'fold_4'}
        self.folds = list(range(5))
        self.folds_nums = list(range(5))
        self.folds_keys = list(self.folds_map.values())
        self.info = 'TBA'
        self.path = os.path.join(CODE_PATH, 'datasets', f'ub_{name}.json')
        self.loaded = False
        self.inputs = self.outputs = self.splits = None
        self.results = DATASETS_RESULTS

    def record(self, fold, predictions, **kwargs):
        predictions = torch.tensor(predictions).view(-1)

        fold_key = self.folds_map[fold]
        keys = self.splits[fold_key]['test']
        test_outputs = torch.tensor(self.outputs[keys]).view(-1)
        mae = L1Loss()(predictions, test_outputs).item()
        mse = MSELoss()(predictions, test_outputs).item()
        rmse = np.sqrt(mse)
        print(f'TASK {self.dataset_name} FOLD {fold} RESULTS: MAE = {mae:.4f}, RMSE = {rmse:.4f}')

        predictions = predictions.tolist()
        try:
            with open('UB_results.json') as f:
                all_results = json.load(f)
        except FileNotFoundError:
            all_results = DATASETS_RESULTS
        all_results[self.dataset_name][self.folds_map[fold]] = predictions
        with open('UB_results.json', 'w+') as f:
            json.dump(all_results, f)
        self.results = all_results

    def load(self):
        with open(self.path) as f:
            dataset = json.load(f)
        self.inputs, self.outputs = load_dataset(dataset, self.dataset_name)
        with open(os.path.join(CODE_PATH, 'datasets', 'metadata_validation.json')) as f:
            self.splits = json.load(f)['splits'][self.dataset_name]

    def get_train_and_val_data(self, fold, as_type='tuple'):
        fold_key = self.folds_map[fold]
        keys = self.splits[fold_key]['train']
        if as_type == 'tuple':
            return self.inputs[keys], self.outputs[keys]
        elif as_type == 'df':
            return pd.concat([self.inputs[keys], self.outputs[keys]], axis=1)

    def get_test_data(self, fold, include_target=False, as_type='tuple'):
        fold_key = self.folds_map[fold]
        keys = self.splits[fold_key]['test']
        if include_target:
            if as_type == 'tuple':
                return self.inputs[keys], self.outputs[keys]
            elif as_type == 'df':
                return pd.concat([self.inputs[keys], self.outputs[keys]], axis=1)
        else:
            return self.inputs[keys]

    @classmethod
    def from_dict(cls, d):
        """Create a MatbenchTask from a dictionary input, from matbench.

        Required method from MSONable.

        Args:
            d (dict):

        Returns:
            (MatbenchTask): The MatbenchTask object.

        """
        req_base_keys = [
            "@module",
            "@class",
            'dataset_name',
            'results',
            'benchmark_name',
        ]
        for k in req_base_keys:
            if k not in d:
                raise KeyError(f"Required key '{k}' not found.")
        extra_base_keys = [k for k in d.keys() if k not in req_base_keys]
        if extra_base_keys:
            raise KeyError(f"Extra keys {extra_base_keys} not allowed.")
        return cls._from_args(
            dataset_name=d['dataset_name'],
            benchmark_name=d['benchmark_name'],
            results_dict=d['results'],
        )

    @classmethod
    def _from_args(cls, dataset_name, benchmark_name, results_dict):
        """Instantiate a MatbenchTask from a arguments, from matbench

        Args:
            dataset_name (str): The name of the dataset/task
            benchmark_name (str): The name of the corresponding benchmark
            results_dict (dict): A formatted dictionary of raw results.

        Returns:
            (MatbenchTask): The matbench task object.
        """
        obj = cls(dataset_name, autoload=False, benchmark=benchmark_name)
        # obj.validate()
        return obj

    def as_dict(self):
        """Return a MatbenchTask object as a dictionary, from matbench.

        Required method from MSONAble.

        Returns:
            (dict): The object as a serialized dictionary.
        """
        return {
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
            'benchmark_name': self.benchmark_name,
            'dataset_name': self.dataset_name,
            'results': dict(self.results),
        }


class DatasetsTasks:
    def __init__(self):
        self.DATASETS_TASKS = {}
        for k in DATASETS_LEN.keys():
            self.DATASETS_TASKS[k] = Task(k)

    def get_tasks(self):
        return self.DATASETS_TASKS
