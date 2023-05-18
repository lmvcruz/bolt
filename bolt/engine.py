from abc import abstractmethod
from typing import Any, List

from bolt.runner import Runner
from bolt.report import SingleExecutionReport

class Engine:
    def __init__(self) -> None:
        self.runners: List[Runner] = []

    def add_runner(self, runner: Runner) -> None:
        self.runners.append(runner)

    @abstractmethod
    def run(self):
        # Run method returns a report (a dataclass object)
        # Different engine implementations might have different
        # implementations of the report data
        raise NotImplementedError()


class SingleExecutionEngine(Engine):
    def __init__(self, input: dict) -> None:
        super().__init__()
        self.input = input

    def run(self):
        report = SingleExecutionReport()
        for runner in self.runners:
            report.input = self.input
            report.tasks[runner.name] = runner.run(self.input)
        return report

