from pprint import pprint


class ProgramReport:
    def __init__(self) -> None:
        self.cases = []
        self.metrics = {}

    def __repr__(self) -> str:
        rep = {}

        if self.metrics:
            rep.update(self.metrics)

        if self.cases:
            rep["cases"] = self.cases

        return str(rep)

    def add_case(self, case):
        self.cases.append(case)

    def add_metric(self, metric_name, value):
        self.metrics[metric_name] = value


class Report:
    def __init__(self) -> None:
        self.programs_report = {}

    def add_program(self, prog_name):
        self.programs_report[prog_name] = ProgramReport()

    def add_program_report_case(self, prog_name, case):
        self.programs_report[prog_name].add_case(case)

    def add_program_metric(self, prog_name, metric, acc):
        self.programs_report[prog_name].add_metric(metric, acc)

    def show(self):
        pprint(self.programs_report)
