from bolt.engine import Engine
from bolt.parameter import Parameter
from bolt.program import Program


class FibonacciProgram(Program):
    def __init__(self) -> None:
        super().__init__()

    def run(self, input: Parameter):
        return Parameter({"result": self.calculate(input["index"])})

    def calculate(self, _):
        raise NotImplementedError()


class NaiveFibonacci(FibonacciProgram):
    def __init__(self) -> None:
        super().__init__()

    def calculate(self, n):
        if n < 2:
            return 1
        return self.calculate(n - 1) + self.calculate(n - 2)


class DpFibonacci(FibonacciProgram):
    def __init__(self) -> None:
        super().__init__()
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


class IteratorFibonacci(FibonacciProgram):
    def __init__(self) -> None:
        super().__init__()

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


def execute_naive_fibonacci(indices):
    engine = Engine()
    prog = NaiveFibonacci()
    engine.add_program(prog)
    for inp in indices:
        input = Parameter({"index": inp})
        engine.add_input(input)
    engine.run()
    print(engine.execution_output)


def main():
    execute_naive_fibonacci([0, 1, 2, 3, 4, 5, 6, 7, 8])


if __name__ == "__main__":
    main()
