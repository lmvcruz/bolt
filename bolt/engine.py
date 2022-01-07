from typing import List

from bolt.parameter import Parameter
from bolt.program import Program


class Engine:
    def __init__(self) -> None:
        self.__programs = []
        self.__inputs = []
        self.__exec_outputs = []

    def add_program(self, prog: Program):
        self.__programs.append(prog)

    def add_input(self, inp: Parameter):
        self.__inputs.append(inp)

    @property
    def execution_output(self) -> List[Parameter]:
        return self.__exec_outputs

    def run(self):
        for prog in self.__programs:
            for inp in self.__inputs:
                self.__exec_outputs.append(prog.run(inp))
