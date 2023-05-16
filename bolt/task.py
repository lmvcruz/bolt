
from abc import abstractmethod


class Task:
    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def run(self, parameters: dict) -> str:
        return ""

    @abstractmethod
    def teardown(self) -> None:
        pass
