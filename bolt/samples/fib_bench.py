from bolt.metrics import ExactDictComparisonMetric
from bolt.program import ProgramController
from bolt.tests.programs.fibonacci import DpFibonacci
from bolt.tests.programs.fibonacci import IteratorFibonacci
from bolt.tests.programs.fibonacci import NaiveFibonacci


def run_program(prog, input, metric):
    controller = ProgramController()
    controller.set_program(prog)
    controller.add_metric(metric)
    controller.run(input)
    metrics = controller.to_dict()
    if metrics[ExactDictComparisonMetric.NAME]:
        print("Ok!")
    else:
        print(f"Fail: {controller.output}")


def estimate_fibonnaci(prog, input):
    controller = ProgramController()
    controller.set_program(prog)
    controller.run(input)
    result = controller.output["results"]
    for idx, fib in zip(input["indices"], result):
        print(f"Fib {idx} = {fib}")
    print(f"Execution time: {controller.execution_time}")


def main():
    input = {
        "indices": [0, 1, 2, 3, 4, 5, 6, 7, 8]
    }
    output = ExactDictComparisonMetric({
        "results": [1, 1, 2, 3, 5, 8, 13, 21, 34]
    })
    run_program(NaiveFibonacci(), input, output)
    run_program(DpFibonacci(), input, output)
    run_program(IteratorFibonacci(), input, output)
    #
    input["indices"] = [1, 10, 30]
    estimate_fibonnaci(NaiveFibonacci(), input)
    input["indices"] = [1, 10, 30, 50, 80, 100, 300, 500, 800]
    estimate_fibonnaci(DpFibonacci(), input)
    input["indices"] = [1, 10, 30, 50, 80, 100, 300, 500, 800,
                        1000, 3000, 5000, 8000, 10000]
    estimate_fibonnaci(IteratorFibonacci(), input)


if __name__ == "__main__":
    main()
