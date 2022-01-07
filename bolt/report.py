from pprint import pprint


class ProgramReport:
    def __init__(self) -> None:
        self.cases = []
        self.accuracy = None

    def __repr__(self) -> str:
        rep = {}

        if self.accuracy:
            rep["accuracy"] = self.accuracy

        if self.cases:
            rep["cases"] = self.cases

        return str(rep)

    def add_case(self, case):
        self.cases.append(case)

    def set_accuracy(self, acc):
        self.accuracy = acc


class Report:
    def __init__(self) -> None:
        self.programs_report = {}

    def add_program(self, prog_name):
        self.programs_report[prog_name] = ProgramReport()

    def add_program_report_case(self, prog_name, case):
        self.programs_report[prog_name].add_case(case)

    def set_program_accuracy(self, prog_name, acc):
        self.programs_report[prog_name].set_accuracy(acc)

    def show(self):
        pprint(self.programs_report)
        # for prog in self.programs_report:
        #     pprint(self.programs_report[prog])
