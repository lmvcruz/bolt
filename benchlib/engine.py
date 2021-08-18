import time
import psutil

from benchlib.metrics import Metric
from benchlib.parameter import Parameter
from benchlib.program import Program


class Engine:
    def __init__(self) -> None:
        self.metric = None
        self.program = None
        #
        self.execution_time = 0
        self.memory = 0
        self.output = None
        self.execution_evaluation = None

    def setMetric(self, met: Metric):
        self.metric = met

    def setProgram(self, prog: Program):
        self.program = prog

    def run(self, input: Parameter = {}):
        start = time.time()
        self.output = self.program.run(input)
        self.execution_time = time.time() - start
        self.memory = psutil.Process().memory_info().rss
        self.execution_evaluation = self.metric.evaluate(self.output)
