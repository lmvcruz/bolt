import math
import os
import sys
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

from benchlib.engine import Engine
from benchlib.metrics import ExactDictComparisonMetric
from benchlib.parameter import Parameter
from benchlib.program import Program

eps = 0.0001
max_counter = 1000


class RootFinderProgram(Program):
    def __init__(self) -> None:
        super().__init__()
        self.root = None
        self.iters = 0
        self.evaluate_function = None

    def exec(self, input: Parameter):
        init = input["init"]
        end = input["end"]
        self.evaluateFunction = eval(input["func"])
        self.findRoot(init, end)
        return {
            "root": self.root,
            "iterations": self.iters,
            "precision": self.evaluateFunction(self.root),
        }

    def evaluateDerivative(self, x):
        return (self.evaluateFunction(x + eps) - self.evaluateFunction(x)) / eps

    def findRoot(self, init, end):
        pass


class NewtonRootFinder(RootFinderProgram):
    def __init__(self) -> None:
        super().__init__()

    def findRoot(self, init, end):
        self.root = (init + end) / 2
        while self.iters < max_counter and abs(self.evaluateFunction(self.root)) > eps:
            func = self.evaluateFunction(self.root)
            der = self.evaluateDerivative(self.root)
            self.root -= func / der
            self.iters += 1


class SubdivisionRootFinder(RootFinderProgram):
    def __init__(self) -> None:
        super().__init__()

    def findRoot(self, init, end):
        self.root = (init + end) / 2
        self.iters += 1
        if abs(self.evaluateFunction(self.root)) < eps or self.iters >= max_counter:
            return
        else:
            if self.evaluateFunction(init)*self.evaluateFunction(self.root) > 0:
                self.findRoot(self.root, end)
            else:
                self.findRoot(init, self.root)


def estimateRootFinder(prog, input):
    engine = Engine()
    engine.setProgram(prog)
    for case in input["cases"]:
        engine.run(case)
        print(engine.output)
        print(f"Execution time: {engine.execution_time}")


if __name__ == "__main__":
    input = {
        "cases": [
            {
                "init": 1,
                "end": 3,
                "func": "lambda x: math.pow(x-0.0001, 2) - 3.2"
            },
            {
                "init": 0,
                "end": 3,
                "func": "lambda x: math.sin(x-1)"
            },
            {
                "init": 0,
                "end": 2,
                "func": "lambda x: math.tan(x-1)"
            },
            {
                "init": -3.5,
                "end": -1,
                "func": "lambda x: math.pow(math.exp(x-1), 2) - math.tan(x-1)"
            },
        ]
    }
    estimateRootFinder(NewtonRootFinder(), input)
    estimateRootFinder(SubdivisionRootFinder(), input)

