import unittest

from benchlib.engine import Engine
from benchlib.metrics import ExactDictComparisonMetric, EmptyMetric, Metric
from benchlib.parameter import Parameter
from benchlib.program import Program

class MockProgram(Program):
    def __init__(self) -> None:
        super().__init__()
        self.mem = []

    def run(self, input: Parameter):
        self.result = {
            "result": 2, 
            "index": input["index"]}
        self.mem = [i for i in range(1000000)]
        return self.result

class EngineTest(unittest.TestCase):
    def test_eval_empty_engine(self):
        engine = Engine()
        engine.setInput(Parameter())
        engine.setMetric(EmptyMetric())
        engine.setProgram(Program())
        engine.run()
        self.assertEqual(engine.execution_evaluation, True)

    def test_mock_program(self):
        engine = Engine()
        engine.setInput({"index": 3})
        engine.setMetric(ExactDictComparisonMetric({"result": 2, "index": 3}))
        prog = MockProgram()
        engine.setProgram(prog)
        self.assertEqual(engine.execution_time, 0)
        engine.run()
        self.assertEqual(engine.execution_evaluation, True)
        self.assertGreater(engine.execution_time, 0.02)
        # Memory bigger than 8*10MB: A list with 1M integer objects was added 
        self.assertGreater(engine.memory, 8*1024*1024)
        self.assertEqual(len(prog.mem), 1000000)


if __name__ == '__main__':
    unittest.main()