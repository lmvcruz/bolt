import unittest

from benchlib.engine import Engine
from benchlib.metrics import ExactDictComparisonMetric, EmptyMetric, Metric
from benchlib.parameter import Parameter
from benchlib.program import Program

class MockProgram(Program):
    def __init__(self) -> None:
        super().__init__()
        self.mem = []

    def exec(self, input: Parameter):
        self.mem = [i for i in range(1000000)]
        return {
            "result": 2, 
            "index": input["index"]}


class EngineTest(unittest.TestCase):
    def test_eval_empty_engine(self):
        engine = Engine()
        engine.setProgram(Program())
        engine.run()
        self.assertEqual(engine.evaluate_output(EmptyMetric()), True)

    def test_mock_program(self):
        prog = MockProgram()
        metric = ExactDictComparisonMetric({"result": 2, "index": 3})
        #
        engine = Engine()
        engine.setProgram(prog)
        self.assertEqual(engine.execution_time, 0)
        #
        engine.run({"index": 3})       
        self.assertEqual(engine.evaluate_output(metric), True)
        self.assertGreater(engine.execution_time, 0.02)
        # Memory bigger than 8*10MB: A list with 1M integer objects was added 
        self.assertGreater(engine.memory, 8*1024*1024)
        self.assertEqual(len(prog.mem), 1000000)


if __name__ == '__main__':
    unittest.main()