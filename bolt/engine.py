from abc import abstractmethod
from typing import List

from bolt.runner import Runner
from bolt.report import SingleExecutionReport

class Engine:
    def __init__(self) -> None:
        self.runners: List[Runner] = []

    def add_runner(self, runner):
        self.runners.append(runner)

    @abstractmethod
    def run(self):
        raise NotImplementedError()


class SingleExecutionEngine(Engine):
    def __init__(self) -> None:
        super().__init__()
        self.input = {}

    def add_input(self, name, value):
        self.input[name] = value

    def run(self):
        report = SingleExecutionReport()
        for runner in self.runners:
            report.input = self.input
            report.tasks[runner.name] = runner.run(self.input)
        return report

