import os
import sys
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

from benchlib.engine import Engine
from benchlib.metrics import ExactDictComparisonMetric
from benchlib.parameter import Parameter
from benchlib.program import Program


class FibonacciProgram(Program):
    def __init__(self) -> None:
        super().__init__()

    def exec(self, input: Parameter):
        indices = input["indices"]
        fibs = {"results": []}
        for idx in indices:
            fibs["results"].append(self.calculate(idx))
        return fibs

    def calculate(self, n):
        pass

class NaiveFibonacci(FibonacciProgram):
    def __init__(self) -> None:
        super().__init__()

    def calculate(self, n):
        if n<2:
            return 1
        return self.calculate(n-1) + self.calculate(n-2)


class DpFibonacci(FibonacciProgram):
    def __init__(self) -> None:
        super().__init__()
        self.memo = {}

    def calculate(self, n):
        if n<2:
            return 1
        if n in self.memo:
            return self.memo[n]
        n1 = self.memo[n-1] if n-1 in self.memo else self.calculate(n-1)
        n2 = self.memo[n-2] if n-2 in self.memo else self.calculate(n-2)
        self.memo[n] = n1 + n2
        return self.memo[n]


class IteratorFibonacci(FibonacciProgram):
    def __init__(self) -> None:
        super().__init__()

    def calculate(self, n):
        if n<2:
            return 1
        n1 = 1
        n2 = 1
        fib = n1 + n2
        for i in range(n+1)[3:]:
            n1 = n2
            n2 = fib
            fib = n1 + n2
        return fib


def runProgram(prog, input, output):
    engine = Engine()
    engine.setProgram(prog)
    engine.run(input)
    if engine.evaluate_output(output):
        print("Ok!")
    else:
        print(f"Fail: {engine.output}")


def estimateFibonnaci(prog, input):
    engine = Engine()
    engine.setProgram(prog)
    engine.run(input)
    result = engine.output["results"]
    for idx, fib in zip(input["indices"], result):
        print(f"Fib {idx} = {fib}")
    print(f"Execution time: {engine.execution_time}")


if __name__ == "__main__":
    input = {
        "indices": [0, 1, 2, 3, 4, 5, 6, 7, 8]
    }
    output = ExactDictComparisonMetric({
        "results": [1, 1, 2, 3, 5, 8, 13, 21, 34]
    })
    runProgram(NaiveFibonacci(), input, output)
    runProgram(DpFibonacci(), input, output)
    runProgram(IteratorFibonacci(), input, output)
    #
    input["indices"] = [1, 10, 30]
    estimateFibonnaci(NaiveFibonacci(), input)
    input["indices"] = [1, 10, 30, 50, 80, 100, 300, 500, 800]
    estimateFibonnaci(DpFibonacci(), input)
    input["indices"] = [1, 10, 30, 50, 80, 100, 300, 500, 800, 
                        1000, 3000, 5000, 8000, 10000]
    estimateFibonnaci(IteratorFibonacci(), input)
