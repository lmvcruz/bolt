import unittest

from bolt.engine import Engine
from bolt.parameter import Parameter
from bolt.samples.mockprog import MockProgram
from bolt.samples.fibonacci import NaiveFibonacci


class EngineTest(unittest.TestCase):
    def test_run_mock_program_with_engine(self):
        engine = Engine()
        prog = MockProgram()
        engine.add_program(prog)
        engine.add_input(None)
        engine.add_input(None)
        engine.run()
        report = engine.report
        self.assertEqual(len(report.programs_report), 1)
        self.assertEqual(len(report.programs_report["Mock"].cases), 2)
        self.assertEqual(
            report.programs_report["Mock"].cases[0]["output"], {"result": 1}
        )
        self.assertEqual(
            report.programs_report["Mock"].cases[1]["output"], {"result": 1}
        )

    def test_run_naive_fibonacci_with_engine(self):
        engine = Engine()
        prog = NaiveFibonacci()
        engine.add_program(prog)
        engine.add_input(Parameter({"index": 0}))
        engine.add_input(Parameter({"index": 4}))
        engine.run()
        report = engine.report
        self.assertEqual(len(report.programs_report), 1)
        self.assertEqual(len(report.programs_report["NaiveFibonacci"].cases), 2)
        self.assertEqual(
            report.programs_report["NaiveFibonacci"].cases[0]["output"], {"result": 1}
        )
        self.assertEqual(
            report.programs_report["NaiveFibonacci"].cases[1]["output"], {"result": 5}
        )


if __name__ == "__main__":
    unittest.main()
