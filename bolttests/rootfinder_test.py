import os
import sys
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

import unittest

from benchlib.engine import Engine
from bolttests.programs.rootfinder import NewtonRootFinder, SubdivisionRootFinder


class RootFinderTest(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.input = {
            "cases": [
                {
                    "init": 1,
                    "end": 3,
                    "func": "lambda x: math.pow(x-0.0001, 2) - 3.2"
                },
                {
                    "init": 0,
                    "end": 3,
                    "func": "lambda x: math.sin(x-1)"
                },
                {
                    "init": 0,
                    "end": 2,
                    "func": "lambda x: math.tan(x-1)"
                },
                {
                    "init": -3.5,
                    "end": -1,
                    "func": "lambda x: math.pow(math.exp(x-1), 2) - math.tan(x-1)"
                },
            ]
        }

    def test_validate_newton_rootfinder(self):
        # TODO: refactor to validate output
        prog = NewtonRootFinder()
        engine = Engine()
        engine.setProgram(prog)
        #
        self.assertEqual(engine.execution_time, 0)
        for case in self.input["cases"]:
            engine.run(case)       
            print(engine.output)

    def test_validate_subdivision_rootfinder(self):
        # TODO: refactor to validate output
        prog = SubdivisionRootFinder()
        engine = Engine()
        engine.setProgram(prog)
        #
        self.assertEqual(engine.execution_time, 0)
        for case in self.input["cases"]:
            engine.run(case)       
            print(engine.output)
