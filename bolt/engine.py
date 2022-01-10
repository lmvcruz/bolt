from typing import List

from bolt import Parameter
from bolt.program import Program
from bolt.metrics import Metric
from bolt.report import Report


class Engine:
    def __init__(self) -> None:
        self.__programs: List[Program] = []
        self.__inputs: List[Parameter] = []
        self.__expected_output: List[Parameter] = []
        self.__exec_metrics: List[Metric] = []
        self.__results_metrics: List[Metric] = []
        self.report = Report()
        self.comprehensive_report = Report()

    def add_program(self, prog: Program) -> None:
        self.__programs.append(prog)
        self.report.add_program(prog.name)

    def add_input(self, inp: Parameter) -> None:
        if self.__expected_output:
            raise Exception("Pair of input/output was already added.")
        self.__inputs.append(inp)

    def add_input_and_expected_output(self, inp: Parameter, out: Parameter) -> None:
        self.__inputs.append(inp)
        self.__expected_output.append(out)

    def add_execution_metric(self, metric: Metric) -> None:
        self.__exec_metrics.append(metric)

    def add_results_metrics(self, metric: Metric) -> None:
        self.__results_metrics.append(metric)

    def run(self) -> None:
        for prog in self.__programs:
            for idx, inp in enumerate(self.__inputs):
                self.__run_metrics_setup(idx)
                out = prog.run(inp)
                case = {"input": inp, "output": out}
                case = self.__run_metrics_teardown(out)
                case["input"] = inp
                self.report.add_program_report_case(prog.name, case)
                if self.__expected_output:
                    case["expected"] = self.__expected_output[idx]

    def add_comprehensive_average_metric_report(self, metric_name):
        for prog in self.report.programs_report:
            self.comprehensive_report.add_program(prog)
            correct_cases = 0
            quantity_cases = 0
            for case in self.report.programs_report[prog].cases:
                correct_cases += case[metric_name]
                quantity_cases += 1

            prog_accur = float(correct_cases) / float(quantity_cases)
            self.comprehensive_report.add_program_metric(prog, metric_name, prog_accur)

    def __run_metrics_setup(self, idx):
        for metric in self.__exec_metrics:
            metric.setup()

        for i in range(len(self.__results_metrics)):
            self.__results_metrics[i].setup(self.__expected_output[idx])

    def __run_metrics_teardown(self, out):
        case = {"output": out}
        for metric in self.__exec_metrics:
            metric.teardown()
            case[metric.NAME] = metric.value

        for metric in self.__results_metrics:
            metric.teardown(out)
            case[metric.NAME] = metric.value

        return case

