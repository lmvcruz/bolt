import pytest
import time

from bolt.metric import ExecutionTimeMetric


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
