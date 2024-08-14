from task import DatasetsTasks


class UnconvbenchBenchmark:
    def __init__(self, **kwargs):
        dt = DatasetsTasks()
        self.DATASETS_TASKS = dt.get_tasks()
        for k in self.DATASETS_TASKS.keys():
            setattr(self, k, self.DATASETS_TASKS[k])

    @property
    def tasks(self):
        return self.DATASETS_TASKS.values()

    def from_preset(self, name, type='', **kwargs): # need implementation
        return self

    def add_metadata(self, metadata, **kwargs): # need implementation
        return 0

    def to_file(self, path, **kwargs): # need implementation
        return 0
