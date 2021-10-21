import unittest

from bolt.program import ProgramController
from bolt.tests.programs.rootfinder import NewtonRootFinder, SubdivisionRootFinder


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
        controller = ProgramController()
        controller.set_program(prog)
        #
        self.assertEqual(controller.execution_time, 0)
        for case in self.input["cases"]:
            controller.run(case)
            print(controller.output)

    def test_validate_subdivision_rootfinder(self):
        # TODO: refactor to validate output
        prog = SubdivisionRootFinder()
        controller = ProgramController()
        controller.set_program(prog)
        #
        self.assertEqual(controller.execution_time, 0)
        for case in self.input["cases"]:
            controller.run(case)
            print(controller.output)


if __name__ == '__main__':
    unittest.main()
