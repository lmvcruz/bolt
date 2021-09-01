import os
import sys
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

import unittest

from benchlib.engine import Engine
from benchlib.metrics import ExactDictComparisonMetric, EmptyMetric
from benchlib.program import Program
from bolttests.programs.mockprog import MockProgram


class EngineTest(unittest.TestCase):
    def test_eval_empty_engine(self):
        engine = Engine()
        engine.setProgram(Program())
        engine.run()
        self.assertEqual(engine.evaluate_output(EmptyMetric()), True)

    def test_mock_program_no_memory(self):
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
        # Memory used by a default infrastructure (18MB)
        self.assertGreater(engine.memory, 18000000)

    def test_mock_program_consuming_memory(self):
        prog = MockProgram([i for i in range(1000000)])
        metric = ExactDictComparisonMetric({"result": 2, "index": 3})
        engine = Engine()
        engine.setProgram(prog)
        #
        self.assertEqual(engine.execution_time, 0)
        engine.run({"index": 3})       
        self.assertEqual(engine.evaluate_output(metric), True)
        self.assertGreater(engine.execution_time, 0.02)
        # Memory bigger than 60MB: ~20MB by default + a list with 1M integer objs 
        # that was emperically observed arounf 40MB
        self.assertGreater(engine.memory, 60000000)
        self.assertEqual(len(prog.mem), 1000000)


if __name__ == '__main__':
    unittest.main()
