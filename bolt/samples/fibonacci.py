from abc import abstractmethod

from bolt.task import Task

class FibonacciTask(Task):
    """A FibonacciTask is the generalization of different tasks
    that implements the algorithm to calculate the k-th Fibonacci number

    Observe that k starts as 0, so the list is:
    0: 1
    1: 1
    2: 2
    3: 3
    4: 5
    5: 8
    6: 13

    The "k" parameter is provided in the field "index" of the input
    """
    def __init__(self, name) -> None:
        super().__init__(name)

    def run(self, input: dict) -> str:
        return self.calculate(input["index"])

    @abstractmethod
    def calculate(self, _):
        raise NotImplementedError()


class NaiveFibonacci(FibonacciTask):
    def __init__(self) -> None:
        super().__init__(NaiveFibonacci.__name__)

    def calculate(self, n):
        if n < 2:
            return 1
        return self.calculate(n - 1) + self.calculate(n - 2)


class DpFibonacci(FibonacciTask):
    def __init__(self) -> None:
        super().__init__(DpFibonacci.__name__)
        self.memo = {}

    def calculate(self, n):
        if n < 2:
            return 1
        if n in self.memo:
            return self.memo[n]
        n1 = self.memo[n - 1] if n - 1 in self.memo else self.calculate(n - 1)
        n2 = self.memo[n - 2] if n - 2 in self.memo else self.calculate(n - 2)
        self.memo[n] = n1 + n2
        return self.memo[n]


class IteratorFibonacci(FibonacciTask):
    def __init__(self) -> None:
        super().__init__(IteratorFibonacci.__name__)

    def calculate(self, n):
        if n < 2:
            return 1
        n1 = 1
        n2 = 1
        fib = n1 + n2
        for _ in range(n + 1)[3:]:
            n1 = n2
            n2 = fib
            fib = n1 + n2
        return fib