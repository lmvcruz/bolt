import unittest

from bolt.metrics import EmptyMetric, ExactDictComparisonMetric
from bolt.metrics import ExecutionTimeMetric, MemoryConsumption
from bolt.program import Program, ProgramController
from bolt.tests.programs.mockprog import MockProgram


class ProgramControllerTest(unittest.TestCase):
    """
        ProgramControllerTest presents behaviour tests for creation, setting,
        and running.

        Setup and teardown are tested along with the run method. The expected
        behaviour is evaluated, since without a direct call of these methods
        in a behaviour test case.
    """
    def test_eval_empty_controller(self):
        controller = ProgramController()
        self.assertEqual(controller.program, None)
        self.assertEqual(controller.metrics, [])
        self.assertEqual(controller.execution_time, 0)
        self.assertEqual(controller.memory, 0)
        self.assertEqual(controller.output, None)
        controller.set_program(Program())
        self.assertTrue(isinstance(controller.program, Program))
        controller.add_metric(EmptyMetric())
        self.assertEqual(controller.metrics[0].NAME, EmptyMetric.NAME)
        self.assertRaises(NotImplementedError, controller.run)
        self.assertEqual(controller.to_dict(),
                         {'output': None, EmptyMetric.NAME: None})

    def test_mock_program_no_memory(self):
        controller = ProgramController()
        prog = MockProgram()
        controller.set_program(prog)
        controller.add_metric(ExactDictComparisonMetric({"result": 2, "index": 3}))
        time_metric = ExecutionTimeMetric()
        self.assertEqual(time_metric.execution_time, None)
        controller.add_metric(time_metric)
        controller.add_metric(MemoryConsumption())
        controller.run({"index": 3})
        metrics = controller.to_dict()
        self.assertGreater(metrics[ExecutionTimeMetric.NAME], 0.02)
        self.assertLess(metrics[MemoryConsumption.NAME], 1)

    def test_mock_program_consuming_memory(self):
        controller = ProgramController()
        prog = MockProgram()
        controller.set_program(prog)
        controller.add_metric(ExactDictComparisonMetric({"result": 2, "index": 3}))
        time_metric = ExecutionTimeMetric()
        self.assertEqual(time_metric.execution_time, None)
        controller.add_metric(time_metric)
        controller.add_metric(MemoryConsumption())
        controller.run({"index": 3, "allocate": True})
        metrics = controller.to_dict()
        self.assertGreater(metrics[ExecutionTimeMetric.NAME], 0.02)
        # The 'allocate' field in the input sent to controller.run, enables the program
        # allocates a list of 1M of numbers (from 0 to 1M). It was emperically observed
        # that this list occuppies a space of ~40MB in memory
        self.assertGreater(metrics[MemoryConsumption.NAME], 40000000)


if __name__ == '__main__':
    unittest.main()
