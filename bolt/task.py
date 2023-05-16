
from abc import abstractmethod


class Task:
    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError("Calling a Task abstract method")

    @abstractmethod
    def run(self, parameters: dict) -> str:
        raise NotImplementedError("Calling a Task abstract method")

    @abstractmethod
    def teardown(self) -> None:
        raise NotImplementedError("Calling a Task abstract method")
