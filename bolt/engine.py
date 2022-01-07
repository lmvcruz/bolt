from typing import List

from bolt import Parameter
from bolt import Program
from bolt.metrics import Metric
from bolt.report import Report


class Engine:
    def __init__(self) -> None:
        self.__programs: List[Program] = []
        self.__inputs: List[Parameter] = []
        self.report = Report()
        self.__exec_metrics: List[Metric] = []

    def add_program(self, prog: Program) -> None:
        self.__programs.append(prog)
        self.report.add_program(prog.name)

    def add_input(self, inp: Parameter) -> None:
        self.__inputs.append(inp)

    def add_execution_metric(self, metric: Metric) -> None:
        self.__exec_metrics.append(metric)

    def run(self) -> None:
        for prog in self.__programs:
            for inp in self.__inputs:
                self.__run_metrics_setup()
                out = prog.run(inp)
                case = {"input": inp, "output": out}
                case = self.__run_metrics_teardown(out)
                case["input"] = inp
                self.report.add_program_report_case(prog.name, case)

    def __run_metrics_setup(self):
        for metric in self.__exec_metrics:
            metric.setup()

    def __run_metrics_teardown(self, out):
        case = {"output": out}
        for metric in self.__exec_metrics:
            metric.teardown()
            case[metric.NAME] = metric.value
        return case
