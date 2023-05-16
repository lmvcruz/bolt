from abc import abstractmethod
import time


class Metric():
    def __init__(self) -> None:
        self.report = {}
        self.name = None

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def teardown(self, _=None):
        pass


class ExecutionTimeMetric(Metric):
    def __init__(self) -> None:
        super().__init__()
        self.start = None
        self.name = "ExecutionTime"

    def setup(self):
        self.start = time.time()

    def teardown(self, _=None):
        self.report["time"] = time.time() - self.start
