from pathlib import Path

from bolt import Parameter
from bolt.program import Program, ExternalProgram
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


# In this function, an engine runs a program (NaiveFibonacci) for serval inputs
# and shows the report with the results, execution time and memory consumption
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


# In this function, the engine runs a program (NaiveFibonacci) for serval inputs
# and validates the output.
# The result of the program execution is a Parameter object where the program
# output is added in the field 'result'. This is an expected standard.
# The comprehensive report is created using the ExactDictComparisonMetric and
# shows the accuracy rate (1.0 == 100%)
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


# In this function, the engine runs several programs for several inputs
# and shows the performance of each program.
# The report allows the user compares this metric
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


# In this function, the engine runs an external program and shows the
# execution report.
# The executable path must be provided to the ExternalProgram object.
def execute_external_fib(indices):
    prog_path = (
        Path(".")
        .joinpath("bolt", "samples", "external_programs", "external_fib.py")
        .absolute()
    )
    prog = ExternalProgram("Naive", prog_path)

    engine = Engine()
    engine.add_execution_metric(ExecutionTimeMetric())
    engine.add_program(prog)
    for idx in indices:
        par = Parameter({"arguments": [str(idx), "NAIVE"]})
        engine.add_input(par)
    engine.run()
    engine.report.show()


# In this function, the engine runs an external program, validates the result
# and shows a comp execution report about the accuracy rate
def validate_external_fib(indices, results):
    prog_path = (
        Path(".")
        .joinpath("bolt", "samples", "external_programs", "external_fib.py")
        .absolute()
    )
    prog = ExternalProgram("Naive", prog_path)

    engine = Engine()
    engine.add_program(prog)
    engine.add_execution_metric(ExecutionTimeMetric())
    comp_metric = ExactDictComparisonMetric()
    comp_metric_name = comp_metric.__class__.NAME
    engine.add_results_metrics(comp_metric)
    for idx, res in zip(indices, results):
        par = Parameter({"arguments": [str(idx), "NAIVE"]})
        expected_out = Parameter({"result": f"{res}\n"})
        engine.add_input_and_expected_output(par, expected_out)
    engine.run()
    engine.add_comprehensive_average_metric_report(comp_metric_name)
    engine.comprehensive_report.show()


def create_specific_engine(engine_name, indices, results):
    prog_path = (
        Path(".")
        .joinpath("bolt", "samples", "external_programs", "external_fib.py")
        .absolute()
    )
    engine = Engine()
    engine.add_program(ExternalProgram(engine_name, prog_path))
    engine.add_execution_metric(ExecutionTimeMetric())
    comp_metric = ExactDictComparisonMetric()
    comp_metric_name = comp_metric.__class__.NAME
    engine.add_results_metrics(comp_metric)
    for idx, res in zip(indices, results):
        par = Parameter({"arguments": [str(idx), engine_name]})
        expected_out = Parameter({"result": f"{res}\n"})
        engine.add_input_and_expected_output(par, expected_out)
    return engine, comp_metric_name


# In this function, we create three engines, each one related to one set of
# argument list (they vary by the algorithm name).
# Each one is executed and its comprehensive report is shown allowing the user
# compares the result
def validate_several_external_fib_progs(indices, results):
    engine_types = ["NAIVE", "DP", "ITERATOR"]
    for eng_type in engine_types:
        engine, comp_metric_name = create_specific_engine(eng_type, indices, results)
        engine.run()
        engine.add_comprehensive_average_metric_report(comp_metric_name)
        engine.comprehensive_report.show()


def main():
    indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 20, 30]
    results = [1, 1, 2, 3, 5, 8, 13, 21, 34, 10946, 1346269]

    execute_naive_fibonacci(indices)
    validate_naive_fibonacci_result(indices, results)
    compare_fibonacci_performance(indices)
    execute_external_fib(indices)
    validate_external_fib(indices, results)
    validate_several_external_fib_progs(indices, results)


if __name__ == "__main__":
    main()
