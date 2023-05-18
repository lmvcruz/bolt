import pytest
import time

from bolt.metric import ExecutionTimeMetric, MemoryConsumption


def test_execution_time_metric_initialization():
    m = ExecutionTimeMetric()
    assert m.name == "ExecutionTime"
    assert m.report == {}
    assert m.start == None


def test_execution_time_measurement():
    m = ExecutionTimeMetric()
    m.setup()
    m.teardown()
    assert 0 < m.report["time"] and m.report["time"] < 1.0e-3

    m.setup()
    time.sleep(1)
    m.teardown()
    assert m.report["time"] > 1


# TODO: This memory consumption behaviour is not a stable implementation
def test_memory_consumption_measurement():
    m = MemoryConsumption()
    assert m.value == None
    m.setup()
    m.teardown()
    assert m.value == 0
    m.setup()
    something = [i for i in range(10000)]
    m.teardown()
    assert m.value > 4000
    assert something == something
