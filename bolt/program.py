from bolt.metrics import Metric
from bolt.parameter import Parameter


class Program:
    def __init__(self) -> None:
        pass

    def exec(self, input: Parameter):
        return None

class ProgramController:
    def __init__(self) -> None:
        self.program = None
        # self.metrics = list[Metric]
        self.metrics = []
        #
        self.execution_time = 0
        self.memory = 0
        self.output = None

    def setProgram(self, prog: Program):
        self.program = prog

    def addMetric(self, m: Metric):
        self.metrics.append(m)

    def setup(self, input):
        for m in self.metrics:
            m.setup(input)

    def teardown(self, output):
        for m in self.metrics:
            m.teardown(output)

    def run(self, input: Parameter = {}):
        self.setup(input)
        self.output = self.program.exec(input)
        self.teardown(self.output)

    def toDict(self):
        d = {
            "output": self.output
        }
        for m in self.metrics:
            d[m.name] = m.value
        return d

    # def evaluate_output(self, metric: Metric):
    #     return metric.evaluate(self.output)
