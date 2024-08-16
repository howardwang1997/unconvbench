# The usage of this package mostly complies with matbench, as shown in this example script

import os
import joblib
import shutil

import torch
from torch.utils.data import DataLoader

from unconvbench.bench import UnconvbenchBenchmark


benchmark = UnconvbenchBenchmark(autoload=False)
# benchmark = benchmark.from_preset('2d_materials')

for task in benchmark.tasks:
    task.load()
    # name = task.dataset_name

    for fold in task.folds:
        # train
        train_inputs, train_outputs = task.get_train_and_val_data(fold)
        # YOUR_MODEL = TRAIN(train_inputs, train_outputs)

        # predict
        test_inputs, test_outputs = task.get_test_data(fold, include_target=True)
        YOUR_PREDICTION = [0.0] * len(test_outputs)
        # YOUR_PREDICTION = PREDICT(YOUR_MODEL, test_inputs)

        # record
        task.record(fold, YOUR_PREDICTION)

hyperparam = None
metadata = {
    "algorithm_version": "1.0.1",
    "hyperparameters": hyperparam
}

benchmark.add_metadata(metadata)
benchmark.to_file("YourModel_UnconvbenchBenchmark.json.gz")
