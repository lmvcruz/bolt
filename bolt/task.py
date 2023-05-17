
from abc import abstractmethod


class Task:
    def __init__(self, name):
        self.name = name

    def setup(self) -> None:
        # A task can have a setup, or not
        pass

    @abstractmethod
    def run(self, parameters: dict) -> str:
        raise NotImplementedError("Calling a Task abstract method")

    def teardown(self) -> None:
        # A task can have a teardown, or not
        pass
