import json

from constant import DATASETS_MAP
from unconvbench_utils import jarvis_dataset_to_mp, make_validation
# NEED REMOVAL


def main():
    for k, v in DATASETS_MAP.items():
        with open(v['path']) as f:
            dataset = json.load(f)
        _ = jarvis_dataset_to_mp(dataset, v['label'], k, save=True)
        print(k, ' done')

    _ = make_validation(random_seed=42, save=True)


if __name__ == '__main__':
    main()
