from bolt.parameter import Parameter
from bolt.program import Program


class MockProgram(Program):
    def __init__(self) -> None:
        super().__init__("Mock")

    def run(self, _: Parameter):
        return Parameter({"result": 1})
