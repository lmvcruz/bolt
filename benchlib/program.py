import time
import psutil

from benchlib.metrics import Metric
from benchlib.parameter import Parameter


class Program:
    def __init__(self) -> None:
        pass

    def exec(self, input: Parameter):
        return None

class ProgramController:
    def __init__(self) -> None:
        self.program = None
        #
        self.execution_time = 0
        self.memory = 0
        self.output = None

    def setProgram(self, prog: Program):
        self.program = prog

    def run(self, input: Parameter = {}):
        start = time.time()
        self.output = self.program.exec(input)
        self.execution_time = time.time() - start
        self.memory = psutil.Process().memory_info().rss

    def evaluate_output(self, metric: Metric):
        return metric.evaluate(self.output)
