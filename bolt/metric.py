from abc import abstractmethod
import time
import psutil


class Metric():
    def __init__(self) -> None:
        self.report = {}
        self.name = None

    @abstractmethod
    def setup(self):
        raise NotImplementedError("Calling a Metric abstract method")

    @abstractmethod
    def teardown(self, _=None):
        raise NotImplementedError("Calling a Metric abstract method")


class ExecutionTimeMetric(Metric):
    def __init__(self) -> None:
        super().__init__()
        self.start = None
        self.name = "ExecutionTime"

    def setup(self):
        self.start = time.time()

    def teardown(self, _=None):
        self.report["time"] = time.time() - self.start


class MemoryConsumption(Metric):
    def __init__(self) -> None:
        super().__init__()
        self.__start = None
        self.__result = None

    def setup(self):
        self.__start = psutil.Process().memory_info().rss

    def teardown(self):
        self.__result = psutil.Process().memory_info().rss - self.__start

    @property
    def value(self):
        return self.__result
