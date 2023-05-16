from bolt.runner import Runner
from bolt.metric import ExecutionTimeMetric

from bolt.samples.k_even_single_exec.keventask import KEvenSingleExecutionTask


def test_execution_time_metric_initialization():
    metric = ExecutionTimeMetric()
    task = KEvenSingleExecutionTask()
    runner = Runner(task)
    runner.add_metric(metric)
    rep = runner.run({"k": 10})
    print(rep)
    exec_time = rep["Metrics"]["ExecutionTime"]["time"]
    assert 0 < exec_time and exec_time < 1e-3
    assert rep["ExecutionOutput"] == "0 2 4 6 8 10 12 14 16 18"
