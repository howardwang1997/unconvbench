from monty.json import MSONable
from matbench.matbench.util import MSONable2File

from .task import DatasetsTasks
from .constant import PRESET_MAPPER


class UnconvbenchBenchmark(MSONable, MSONable2File):
    def __init__(self, **kwargs):
        dt = DatasetsTasks()
        self.DATASETS_TASKS = dt.get_tasks()
        for k in self.DATASETS_TASKS.keys():
            setattr(self, k, self.DATASETS_TASKS[k])

        self.all_tasks = self.DATASETS_TASKS.values()
        self.user_metadata = None

    @property
    def tasks(self):
        return self.all_tasks

    def from_preset(self, subset_type, **kwargs):
        assert subset_type in PRESET_MAPPER.keys()
        self.all_tasks = {k: v for k, v in self.DATASETS_TASKS.items() if k in PRESET_MAPPER[subset_type]}
        return self

    def add_metadata(self, metadata: dict, **kwargs):
        """
        Add dictionary as user metadata
        :param metadata:
        :param kwargs:
        :return: NoneType
        """
        if self.user_metadata:
            print("User metadata already exists! Overwriting...")

        self.user_metadata = metadata
        print("User metadata added successfully!")

    def load(self):
        """Load all tasks in this benchmark.
        Returns:
            (NoneType): Datasets are kept in attributes.
        """
        for t in self.tasks:
            t.load()
