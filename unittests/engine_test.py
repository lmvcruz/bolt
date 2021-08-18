import unittest

from benchlib.engine import Engine
from benchlib.metrics import EmptyMetric, Metric
from benchlib.parameter import Parameter
from benchlib.program import Program

class EmptyEngineTest(unittest.TestCase):
    def test_eval_empty_engine(self):
        engine = Engine()
        engine.setInput(Parameter())
        engine.setMetric(EmptyMetric())
        engine.setProgram(Program())
        engine.run()
        self.assertEqual(engine.execution_evaluation, True)

if __name__ == '__main__':
    unittest.main()