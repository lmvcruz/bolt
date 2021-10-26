# Even it is not explicitely used, it can be used by implicit evaluated functions
import math

from bolt.parameter import Parameter
from bolt.program import Program

EPS = 0.0001
MAX_COUNTER = 1000


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
        return (self.evaluateFunction(x + EPS) - self.evaluateFunction(x)) / EPS

    def findRoot(self, init, end):
        raise NotImplementedError()


class NewtonRootFinder(RootFinderProgram):
    def __init__(self) -> None:
        super().__init__()

    def findRoot(self, init, end):
        self.root = (init + end) / 2
        while self.iters < MAX_COUNTER and abs(self.evaluateFunction(self.root)) > EPS:
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
        if abs(self.evaluateFunction(self.root)) < EPS or self.iters >= MAX_COUNTER:
            return
        else:
            if self.evaluateFunction(init) * self.evaluateFunction(self.root) > 0:
                self.findRoot(self.root, end)
            else:
                self.findRoot(init, self.root)
