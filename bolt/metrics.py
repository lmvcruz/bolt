import math
import time
import psutil

from bolt import Parameter


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


class ExactDictComparisonMetric(Metric):
    NAME = "EXACT_DICT_COMPARISON"

    def __init__(self) -> None:
        super().__init__(ExactDictComparisonMetric.NAME)
        self.__expected = None
        self.__result = None

    def setup(self, expected: Parameter = None):
        self.__expected = expected

    def teardown(self, output: Parameter):
        self.__result = self.__expected == output

    @property
    def value(self):
        return self.__result


class ToleranceComparisonMetric(Metric):
    NAME = "TOLERANCE_COMPARISON"

    def __init__(self, tol=0.01) -> None:
        super().__init__(ToleranceComparisonMetric.NAME)
        self.__tolerance = tol
        self.__expected = None
        self.__result = None

    def setup(self, expected: Parameter = None):
        self.__expected = expected["result"]

    def teardown(self, output: Parameter):
        actual = output["result"]
        self.__result = math.fabs(actual - self.__expected) < self.__tolerance

    @property
    def value(self):
        return self.__result


class AccuracyMetric(Metric):
    NAME = "ACCURACY"

    def __init__(self) -> None:
        super().__init__(AccuracyMetric.NAME)
        self.__expected = None
        self.__result = None

    def setup(self, expected: Parameter = None):
        self.__expected = expected["result"]

    def teardown(self, output: Parameter):
        actual = output["result"]
        self.__result = math.fabs(actual - self.__expected)

    @property
    def value(self):
        return self.__result


class ConfusionMatrixMetric(Metric):
    NAME = "CONFUSION_MATRIX"

    def __init__(self) -> None:
        super().__init__(AccuracyMetric.NAME)
        self.__expected = None
        self.__result = {
            "true_positive": 0,
            "true_negative": 0,
            "false_positive": 0,
            "false_negative": 0,
        }

    def setup(self, expected: Parameter = None):
        self.__expected = expected["result"]

    def teardown(self, output: Parameter):
        actual = output["result"]
        if self.__expected and actual:
            self.__result["true_positive"] += 1
        elif self.__expected and not actual:
            self.__result["false_negative"] += 1
        elif actual:  # expected == False
            self.__result["false_positive"] += 1
        else:  # expected == False and actual == False
            self.__result["true_negative"] += 1

    @property
    def value(self):
        return self.__result
