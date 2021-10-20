import time
import psutil

from bolt.parameter import Parameter


class Metric:
    NAME = "ABSTRACT_METRIC"

    def __init__(self, name="ABSTRACT_METRIC") -> None:
        self.name = name

    # This method is not just the interface. Some specific metrics can do not
    # do nothing in the setup step (then, do not overwrite this method)
    def setup(self, _: Parameter = None):
        pass

    # This method is not just the interface. Some specific metrics can do not
    # do nothing in the teardown step (then, do not overwrite this method)
    def teardown(self, _: Parameter = None):
        pass


class EmptyMetric(Metric):
    NAME = "EMPTY_METRIC"

    def __init__(self) -> None:
        super().__init__(EmptyMetric.NAME)
        self.__result = None

    def teardown(self, output: Parameter):
        self.__result = output is None

    @property
    def value(self):
        return self.__result


class ExactDictComparisonMetric(Metric):
    NAME = "EXACT_DICT_COMPARISON"

    def __init__(self, expected) -> None:
        super().__init__(ExactDictComparisonMetric.NAME)
        self.__expected = expected
        self.__result = None

    def teardown(self, output: Parameter):
        self.__result = self.__expected == output

    @property
    def value(self):
        return self.__result


class ExecutionTimeMetric(Metric):
    NAME = "EXECUTION_TIME"

    def __init__(self) -> None:
        super().__init__(ExecutionTimeMetric.NAME)
        self.start = None
        self.execution_time = None

    def setup(self, _: Parameter = None):
        self.start = time.time()

    def teardown(self, _: Parameter = None):
        self.execution_time = time.time() - self.start

    @property
    def value(self):
        return self.execution_time


class MemoryConsumption(Metric):
    NAME = "MEMORY_CONSUMPTION"

    def __init__(self) -> None:
        super().__init__(MemoryConsumption.NAME)
        self.__start = None
        self.__result = None

    def setup(self, _: Parameter = None):
        self.__start = psutil.Process().memory_info().rss

    def teardown(self, _: Parameter = None):
        self.__result = psutil.Process().memory_info().rss - self.__start

    @property
    def value(self):
        return self.__result
