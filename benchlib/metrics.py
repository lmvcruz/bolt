import time
import psutil

from benchlib.parameter import Parameter


class Metric:
    def __init__(self, name) -> None:
        self.name = name
    
    def setup(self, input: Parameter):
        pass

    def teardown(self, output: Parameter):
        pass

    @property
    def value(self):
        return None

class EmptyMetric(Metric):
    def __init__(self) -> None:
        super().__init__("EmptyMetric")
        self.result = None

    def teardown(self, output: Parameter):
        self.result = output is None

    @property
    def value(self):
        return self.result

class ExactDictComparisonMetric(Metric):
    def __init__(self, expected) -> None:
        super().__init__("ExactDictComparisonMetric")
        self.expected = expected

    def teardown(self, output: Parameter):
        self.result = self.expected == output

    @property
    def value(self):
        return self.result


class ExecutionTimeMetric(Metric):
    def __init__(self) -> None:
        super().__init__("ExecutionTimeMetric")
        self.start = None
        self.execution_time = None
    
    def setup(self, input: Parameter):
        self.start = time.time()

    def teardown(self, output: Parameter):
        self.execution_time = time.time() - self.start

    @property
    def value(self):
        return self.execution_time


class MemoryConsumption(Metric):
    def __init__(self) -> None:
        super().__init__("MemoryConsumption")
        self.start = None
        self.memory = None

    def setup(self, input: Parameter):
        self.start = psutil.Process().memory_info().rss

    def teardown(self, output: Parameter):
        self.memory = psutil.Process().memory_info().rss - self.start

    @property
    def value(self):
        return self.memory