from benchlib.metrics import Metric
from benchlib.parameter import Parameter
from benchlib.program import Program


class Engine:
    def __init__(self) -> None:
        self.input = None
        self.metric = None
        self.program = None
        #
        self.output = None
        self.execution_evaluation = None

    def setInput(self, inp: Parameter):
        self.input = inp

    def setMetric(self, met: Metric):
        self.metric = met

    def setProgram(self, prog: Program):
        self.program = prog

    def run(self):
        self.output = self.program.run(self.input)
        self.execution_evaluation = self.metric.evaluate(self.output)
    