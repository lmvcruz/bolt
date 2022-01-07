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
        expected_output = [Parameter({"result": 1}), Parameter({"result": 1})]
        self.assertEqual(engine.execution_output, expected_output)

    def test_run_naive_fibonacci_with_engine(self):
        engine = Engine()
        prog = NaiveFibonacci()
        engine.add_program(prog)
        engine.add_input(Parameter({"index": 1}))
        engine.add_input(Parameter({"index": 3}))
        engine.run()
        expected_output = [Parameter({"result": 1}), Parameter({"result": 3})]
        self.assertEqual(engine.execution_output, expected_output)


if __name__ == "__main__":
    unittest.main()
