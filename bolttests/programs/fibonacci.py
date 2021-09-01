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
