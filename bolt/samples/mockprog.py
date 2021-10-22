from bolt.parameter import Parameter
from bolt.program import Program


class MockProgram(Program):
    def __init__(self) -> None:
        super().__init__()
        self.mem = []
        self.acm = 0

    def exec(self, input: Parameter):
        if "allocate" in input and input["allocate"]:
            self.mem = [i for i in range(1000000)]
        self.acm = 1
        for i in range(1000000):
            self.acm += i
        return {
            "result": 2,
            "index": input["index"]
        }
