import unittest

from bolt.metrics import EmptyMetric, ExactDictComparisonMetric
from bolt.metrics import ExecutionTimeMetric, MemoryConsumption
from bolt.program import Program, ProgramController
from bolt.tests.programs.mockprog import MockProgram


class ProgramControllerTest(unittest.TestCase):
    def test_eval_empty_controller(self):
        controller = ProgramController()
        controller.setProgram(Program())
        controller.addMetric(EmptyMetric())
        controller.run()
        self.assertEqual(controller.toDict(), {'output': None, 'EmptyMetric': True})

    def test_mock_program_no_memory(self):
        controller = ProgramController()
        #
        prog = MockProgram()
        controller.setProgram(prog)
        #
        controller.addMetric(ExactDictComparisonMetric({"result": 2, "index": 3}))
        time_metric = ExecutionTimeMetric()
        self.assertEqual(time_metric.execution_time, None)
        controller.addMetric(time_metric)
        controller.addMetric(MemoryConsumption())
        #
        #
        controller.run({"index": 3})
        metrics = controller.toDict()
        self.assertGreater(metrics["ExecutionTimeMetric"], 0.02)
        self.assertLess(metrics["MemoryConsumption"], 1)

    def test_mock_program_consuming_memory(self):
        controller = ProgramController()
        #
        prog = MockProgram()
        controller.setProgram(prog)
        #
        controller.addMetric(ExactDictComparisonMetric({"result": 2, "index": 3}))
        time_metric = ExecutionTimeMetric()
        self.assertEqual(time_metric.execution_time, None)
        controller.addMetric(time_metric)
        controller.addMetric(MemoryConsumption())
        #
        controller.run({"index": 3, "allocate": True})
        metrics = controller.toDict()
        self.assertGreater(metrics["ExecutionTimeMetric"], 0.02)
        # The 'allocate' field in the input sent to controller.run, enables the program 
        # allocates a list of 1M of numbers (from 0 to 1M). It was emperically observed 
        # that this list occuppies a space of ~40MB in memory
        self.assertGreater(metrics["MemoryConsumption"], 40000000)



if __name__ == '__main__':
    unittest.main()
