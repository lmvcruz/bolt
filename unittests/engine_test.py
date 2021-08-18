import unittest

from benchlib.engine import Engine
from benchlib.metrics import ExactDictComparisonMetric, EmptyMetric, Metric
from benchlib.parameter import Parameter
from benchlib.program import Program

class MockProgram(Program):
    def __init__(self) -> None:
        super().__init__()

    def run(self, input: Parameter):
        self.result = {
            "result": 2, 
            "index": input["index"]}
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
        engine.setProgram(MockProgram())
        engine.run()
        self.assertEqual(engine.execution_evaluation, True)


if __name__ == '__main__':
    unittest.main()