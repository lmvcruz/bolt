from bolt.runner import Runner
from bolt.metric import ExecutionTimeMetric
from bolt.samples.keventask import KEvenSingleExecutionTask


def test_execution_time_metric_initialization():
    metric = ExecutionTimeMetric()
    task = KEvenSingleExecutionTask()
    runner = Runner(task)
    assert runner.name == "KEvenSingleExecutionTask"
    assert len(runner.metrics) == 0
    runner.add_metric(metric)
    assert len(runner.metrics) == 1
    input = {"k": 10}
    rep = runner.run(input)
    assert rep.input == {"k": 10}
    assert rep.output == "0 2 4 6 8 10 12 14 16 18"
    exec_time = rep.metrics["ExecutionTime"]["time"]
    assert 0 < exec_time and exec_time < 1e-3
