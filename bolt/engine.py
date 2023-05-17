from abc import abstractmethod
from typing import List

from bolt.runner import Runner

class Engine:
    def __init__(self) -> None:
        self.runners: List[Runner] = []
        self.report: dict = {}

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
        for runner in self.runners:
            self.report[runner.name] = runner.run(self.input)

