import datetime
import json
import gzip
import traceback

from monty.json import MSONable
from monty.serialization import dumpfn

from .task import DatasetsTasks, Task
from .constant import PRESET_MAPPER, VERSION
from .utils import immutify_dictionary, hash_dictionary


class UnconvbenchBenchmark(MSONable):
    # fix the keys in next update
    def __init__(self, autoload=False, **kwargs):
        self.benchmark_name = 'unconvbench-1.0.1'
        dt = DatasetsTasks()
        self.DATASETS_TASKS = dt.get_tasks()
        for k in self.DATASETS_TASKS.keys():
            setattr(self, k, self.DATASETS_TASKS[k])

        self.all_tasks = self.DATASETS_TASKS.values()
        self.user_metadata = None

        self.tasks_map = {}

    @property
    def tasks(self):
        return self.all_tasks

    def from_preset(self, subset_type, **kwargs):
        assert subset_type in PRESET_MAPPER.keys(), f'Only subset_type within {list(PRESET_MAPPER.keys())} supported!'
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

    def to_file(self, filename):
        d = self.as_dict()
        dumpfn(d, filename)

    @classmethod
    def from_file(cls, filename):
        if filename.endswith(".gz"):
            with gzip.open(filename, "rb") as f:
                d = json.loads(f.read().decode("utf-8"))
        else:
            with open(filename) as f:
                d = json.load(f)

        return cls.from_dict(d)

    def as_dict(self):
        """Overridden from MSONable.as_dict, get dict repr of this obj

        Returns:
            d (dict): the object as a dictionary.

        """
        tasksd = {mbt.dataset_name: mbt.as_dict() for mbt in self.tasks}
        tasksd_jsonable = immutify_dictionary(tasksd)

        d = {
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
            'version': VERSION,
            'tasks': tasksd_jsonable,
            'user_metadata': self.user_metadata,
            'benchmark_name': self.benchmark_name,
            'datestamp': datetime.datetime.utcnow().strftime(
                '"%Y.%m.%d %H:%M.%S"'
            ),
        }

        # to obtain a hash for this benchmark, immutify the dictionary
        # and then stringify it
        d['hash'] = hash_dictionary(d)
        return d

    @classmethod
    def from_dict(cls, d):
        """Create a MatbenchBenchmark object from a dictionary.

        Args:
            d (dict): The benchmark as a dictionary.

        Returns:
            (MatbenchBenchmark): The benchmark as an object.

        """
        required_keys = [
            "@module",
            "@class",
            'version',
            'benchmark_name',
            'tasks',
            'user_metadata',
            'datestamp',
            'hash',
        ]

        missing_keys = []
        for k in required_keys:
            if k not in d:
                missing_keys.append(k)

        extra_keys = []
        for k in d:
            if k not in required_keys:
                extra_keys.append(k)

        if missing_keys and not extra_keys:
            raise ValueError(
                f"Required keys {missing_keys} for {cls.__class__.__name__} "
                f"not found!"
            )
        elif not missing_keys and extra_keys:
            raise ValueError(
                f"Extra keys {extra_keys} for {cls.__class__.__name__} " f"present!"
            )
        elif missing_keys and extra_keys:
            raise ValueError(
                f"Missing required keys {missing_keys} and extra keys "
                f"{extra_keys} present!"
            )

        # Check all tasks to make sure their benchmark name is matching in the
        # benchmark and in the tasks
        not_matching_bench = []
        for t_dict in d['tasks'].values():
            if t_dict['benchmark_name'] != d['benchmark_name']:
                not_matching_bench.append(t_dict['dataset_name'])
        if not_matching_bench:
            raise ValueError(
                f"Tasks {not_matching_bench} do not have a benchmark name "
                f"matching the benchmark ({d['benchmark_name']})!"
            )

        # Ensure the hash is matching, i.e., the data was not modified after
        # matbench got done with it
        m_from_dict = d.pop('hash')
        m = hash_dictionary(d)
        if m != m_from_dict:
            raise ValueError(
                f"Hash of dictionary does not match it's reported value! {m} "
                f"!= {m_from_dict} . Was the data modified after saving?)"
            )

        # Check to see if any tasks have task names not matching their key
        # names in the benchmark
        not_matching_tasks = []
        for task_name, task_info in d['tasks'].items():
            key_as_per_task = task_info['dataset_name']
            if task_name != key_as_per_task:
                not_matching_tasks.append((task_name, key_as_per_task))
        if not_matching_tasks:
            raise ValueError(
                f"Task names in benchmark and task names in tasks not "
                f"matching: {not_matching_tasks}"
            )

        return cls._from_args(
            benchmark_name=d['benchmark_name'],
            tasks_dict=d['tasks'],
            user_metadata=d['user_metadata'],
        )

    @classmethod
    def _from_args(cls, benchmark_name, tasks_dict, user_metadata):
        """Create a MatbenchBenchmark object from arguments

        Args:
            benchmark_name (str): name of the benchmark
            tasks_dict (dict): formatted dict of task data
            user_metadata (dict): freeform user metadata

        Returns:
            (MatbenchBenchmark)
        """
        subset = list(tasks_dict.keys())
        obj = cls(benchmark=benchmark_name, autoload=False, subset=subset)
        obj.tasks_map = {
                t_name: Task.from_dict(t_dict)
                for t_name, t_dict in tasks_dict.items()
            }

        # MatbenchTask automatically validates files during its from_dict
        obj.user_metadata = user_metadata

        return obj

    def validate(self):
        """Run validation on each task in this benchmark, from matbench.

        Returns:
            ({str: str}): dict of errors, if they exist

        """
        errors = {}
        for t, t_obj in self.DATASETS_TASKS.items():
            try:
                t_obj.validate()
            except BaseException:
                errors[t] = traceback.format_exc()
        return errors

    @property
    def scores(self):
        """Get all score metrics for all tasks as a dictionary, from matbench.

        Returns:
            (RecursiveDotDict): A nested dictionary-like object of scores
                for each task.

        """
        return {t.dataset_name: t.scores for t in self.tasks}
