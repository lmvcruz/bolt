# Even it is not explicitely used, it can be used by implicit evaluated functions
import math

from bolt import Parameter
from bolt import Program
from bolt.engine import Engine
from bolt.metrics import ExecutionTimeMetric, ToleranceComparisonMetric, AccuracyMetric

EPS = 0.0001
MAX_COUNTER = 1000


class RootFinderProgram(Program):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.root = None
        self.iters = 0
        self.evaluate_function = None

    def run(self, input: Parameter):
        init = input["init"]
        end = input["end"]
        self.evaluateFunction = eval(input["func"])
        self.findRoot(init, end)
        return {
            "root": self.root,
            "iterations": self.iters,
            "result": self.evaluateFunction(self.root),
        }

    def evaluateDerivative(self, x):
        return (self.evaluateFunction(x + EPS) - self.evaluateFunction(x)) / EPS

    def findRoot(self, init, end):
        raise NotImplementedError()


class NewtonRootFinder(RootFinderProgram):
    def __init__(self) -> None:
        super().__init__(NewtonRootFinder.__name__)

    def findRoot(self, init, end):
        self.root = (init + end) / 2
        while self.iters < MAX_COUNTER and abs(self.evaluateFunction(self.root)) > EPS:
            func = self.evaluateFunction(self.root)
            der = self.evaluateDerivative(self.root)
            self.root -= func / der
            self.iters += 1


class SubdivisionRootFinder(RootFinderProgram):
    def __init__(self) -> None:
        super().__init__(SubdivisionRootFinder.__name__)

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


def estimate_root_finder(prog, cases):
    engine = Engine()
    engine.add_program(prog)
    engine.add_execution_metric(ExecutionTimeMetric())
    engine.add_results_metrics(ToleranceComparisonMetric())
    expected = Parameter({"result": 0.0})
    for case in cases:
        engine.add_input_and_expected_output(Parameter(case), expected)
    engine.run()
    engine.report.show()


def estimate_root_finder_with_comprehensive_engine(prog, cases):
    engine = Engine()
    engine.add_program(prog)
    engine.add_execution_metric(ExecutionTimeMetric())
    comp_metric = ToleranceComparisonMetric()
    comp_metric_name = comp_metric.__class__.NAME
    engine.add_results_metrics(comp_metric)
    expected = Parameter({"result": 0.0})
    for case in cases:
        engine.add_input_and_expected_output(Parameter(case), expected)
    engine.run()
    engine.add_comprehensive_average_metric_report(comp_metric_name)
    engine.comprehensive_report.show()


def compare_root_finder_accuracy(cases):
    engine = Engine()
    engine.add_program(NewtonRootFinder())
    engine.add_program(SubdivisionRootFinder())
    comp_metric = AccuracyMetric()
    comp_metric_name = comp_metric.__class__.NAME
    engine.add_results_metrics(comp_metric)
    expected = Parameter({"result": 0.0})
    for case in cases:
        engine.add_input_and_expected_output(Parameter(case), expected)
    engine.run()
    engine.report.show()
    engine.add_comprehensive_average_metric_report(comp_metric_name)
    engine.comprehensive_report.show()


def main():
    cases = [
        {"init": 1, "end": 3, "func": "lambda x: math.pow(x-0.0001, 2) - 3.2"},
        {"init": 0, "end": 3, "func": "lambda x: math.sin(x-1)"},
        {"init": 0, "end": 2, "func": "lambda x: math.tan(x-1)"},
        {
            "init": -3.5,
            "end": -1,
            "func": "lambda x: math.pow(math.exp(x-1), 2) - math.tan(x-1)",
        },
    ]
    estimate_root_finder(NewtonRootFinder(), cases)
    estimate_root_finder_with_comprehensive_engine(NewtonRootFinder(), cases)

    estimate_root_finder(SubdivisionRootFinder(), cases)
    estimate_root_finder_with_comprehensive_engine(SubdivisionRootFinder(), cases)

    compare_root_finder_accuracy(cases)


if __name__ == "__main__":
    main()
