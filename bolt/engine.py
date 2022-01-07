from typing import List

from bolt.parameter import Parameter
from bolt.program import Program
from bolt.report import Report


class Engine:
    def __init__(self) -> None:
        self.__programs = []
        self.__inputs = []
        self.report = Report()

    def add_program(self, prog: Program):
        self.__programs.append(prog)
        self.report.add_program(prog.name)

    def add_input(self, inp: Parameter):
        self.__inputs.append(inp)

    def run(self):
        for prog in self.__programs:
            for inp in self.__inputs:
                out = prog.run(inp)
                case = {"input": inp, "output": out}
                self.report.add_program_report_case(prog.name, case)
