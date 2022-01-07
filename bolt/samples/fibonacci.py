from bolt import Parameter
from bolt import Program
from bolt.engine import Engine
from bolt.metrics import (
    ExecutionTimeMetric,
    MemoryConsumption,
    ExactDictComparisonMetric,
)


class FibonacciProgram(Program):
    def __init__(self, name) -> None:
        super().__init__(name)

    def run(self, input: Parameter):
        return Parameter({"result": self.calculate(input["index"])})

    def calculate(self, _):
        raise NotImplementedError()


class NaiveFibonacci(FibonacciProgram):
    def __init__(self) -> None:
        super().__init__(NaiveFibonacci.__name__)

    def calculate(self, n):
        if n < 2:
            return 1
        return self.calculate(n - 1) + self.calculate(n - 2)


class DpFibonacci(FibonacciProgram):
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


class IteratorFibonacci(FibonacciProgram):
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


def execute_naive_fibonacci(indices):
    engine = Engine()
    engine.add_program(NaiveFibonacci())
    engine.add_execution_metric(ExecutionTimeMetric())
    engine.add_execution_metric(MemoryConsumption())
    for inp in indices:
        input = Parameter({"index": inp})
        engine.add_input(input)
    engine.run()
    engine.report.show()


def validate_naive_fibonacci_result(indices, results):
    engine = Engine()
    engine.add_program(NaiveFibonacci())
    engine.add_execution_metric(ExecutionTimeMetric())
    engine.add_execution_metric(MemoryConsumption())
    comp_metric = ExactDictComparisonMetric()
    comp_metric_name = comp_metric.__class__.NAME
    engine.add_results_metrics(comp_metric)
    for idx, res in zip(indices, results):
        input = Parameter({"index": idx})
        expected_out = Parameter({"result": res})
        engine.add_input_and_expected_output(input, expected_out)
    engine.run()
    engine.add_comprehensive_average_metric_report(comp_metric_name)
    engine.comprehensive_report.show()


def compare_fibonacci_performance(indices):
    engine = Engine()
    engine.add_program(NaiveFibonacci())
    engine.add_program(DpFibonacci())
    engine.add_program(IteratorFibonacci())
    comp_metric = ExecutionTimeMetric()
    comp_metric_name = comp_metric.__class__.NAME
    engine.add_execution_metric(comp_metric)
    for inp in indices:
        input = Parameter({"index": inp})
        engine.add_input(input)
    engine.run()
    engine.add_comprehensive_average_metric_report(comp_metric_name)
    engine.comprehensive_report.show()


def main():
    indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 20]
    execute_naive_fibonacci(indices)

    results = [1, 1, 2, 3, 5, 8, 13, 21, 34, 10946]
    validate_naive_fibonacci_result(indices, results)

    compare_fibonacci_performance(indices)


if __name__ == "__main__":
    main()
