from benchlib.parameter import Parameter
from benchlib.program import Program


class MockProgram(Program):
    def __init__(self, m=None) -> None:
        super().__init__()
        self.mem = m
        self.acm = 0

    def exec(self, input: Parameter):
        self.acm = 1
        for i in range(1000000):
            self.acm += i
        return {
            "result": 2, 
            "index": input["index"]}
