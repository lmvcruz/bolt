from pprint import pprint


class ProgramReport:
    def __init__(self) -> None:
        self.cases = []

    def __repr__(self) -> str:
        return str(self.cases)

    def add_case(self, case):
        self.cases.append(case)


class Report:
    def __init__(self) -> None:
        self.programs_report = {}

    def add_program(self, prog_name):
        self.programs_report[prog_name] = ProgramReport()

    def add_program_report_case(self, prog_name, case):
        self.programs_report[prog_name].add_case(case)

    def show(self):
        for prog in self.programs_report:
            pprint(self.programs_report[prog])
