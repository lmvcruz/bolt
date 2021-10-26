import time
import unittest

from bolt.metrics import EmptyMetric
from bolt.metrics import ExactDictComparisonMetric
from bolt.metrics import ExecutionTimeMetric
from bolt.metrics import MemoryConsumption
from bolt.metrics import Metric
from bolt.parameter import Parameter


class MetricTest(unittest.TestCase):
    def test_create_abstract_metric(self):
        m = Metric()
        self.assertEqual(m.name, Metric.NAME)
        self.assertEqual(Metric.NAME, "ABSTRACT_METRIC")

    def test_create_empty_metric(self):
        m = EmptyMetric()
        self.assertEqual(m.name, EmptyMetric.NAME)
        self.assertEqual(EmptyMetric.NAME, "EMPTY_METRIC")
        self.assertEqual(m.value, None)
        m.teardown("")
        self.assertEqual(m.value, False)

    def test_create_exact_dict_comp_metric_with_dict(self):
        d = {
            "name": "foo",
            "first_att": "baa",
            "second_att": 5
        }
        m = ExactDictComparisonMetric(d)
        self.assertEqual(m.name, ExactDictComparisonMetric.NAME)
        self.assertEqual(ExactDictComparisonMetric.NAME, "EXACT_DICT_COMPARISON")
        self.assertEqual(m.value, None)
        m.teardown(d)
        self.assertEqual(m.value, True)

    def test_create_exact_dict_comp_metric_with_parameter(self):
        d = Parameter({
            "name": "foo",
            "first_att": "baa",
            "second_att": 5
        })
        m = ExactDictComparisonMetric(d)
        self.assertEqual(m.name, ExactDictComparisonMetric.NAME)
        self.assertEqual(ExactDictComparisonMetric.NAME, "EXACT_DICT_COMPARISON")
        self.assertEqual(m.value, None)
        m.teardown(d)
        self.assertEqual(m.value, True)

    def test_create_execution_time_metric(self):
        m = ExecutionTimeMetric()
        self.assertEqual(m.name, ExecutionTimeMetric.NAME)
        self.assertEqual(ExecutionTimeMetric.NAME, "EXECUTION_TIME")
        self.assertEqual(m.value, None)
        m.setup()
        m.teardown()
        self.assertLess(m.value, 0.1)
        m.setup()
        time.sleep(0.10001)
        m.teardown()
        self.assertGreater(m.value, 0.1)

    # TODO: This memory consumption behaviour is not a stable implementation
    def test_create_memory_consumption_metric(self):
        m = MemoryConsumption()
        self.assertEqual(m.name, MemoryConsumption.NAME)
        self.assertEqual(MemoryConsumption.NAME, "MEMORY_CONSUMPTION")
        self.assertEqual(m.value, None)
        m.setup()
        m.teardown()
        self.assertEqual(m.value, 0)
        m.setup()
        something = [i for i in range(10000)]
        m.teardown()
        self.assertGreater(m.value, 4000)
        self.assertEqual(something, something)


if __name__ == '__main__':
    unittest.main()
