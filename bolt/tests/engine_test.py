from bolt.engine import SingleExecutionEngine
from bolt.metric import ExecutionTimeMetric
from bolt.runner import Runner
from bolt.samples.fibonacci import NaiveFibonacci, DpFibonacci, IteratorFibonacci

def test_single_exec_engine():
    naive_fib_runner = Runner(NaiveFibonacci())
    naive_fib_runner.add_metric(ExecutionTimeMetric())

    dp_fib_runner = Runner(DpFibonacci())
    dp_fib_runner.add_metric(ExecutionTimeMetric())

    iterator_fib_runner = Runner(IteratorFibonacci())
    iterator_fib_runner.add_metric(ExecutionTimeMetric())

    engine = SingleExecutionEngine()
    engine.add_runner(naive_fib_runner)
    engine.add_runner(dp_fib_runner)
    engine.add_runner(iterator_fib_runner)
    assert len(engine.runners) == 3

    engine.add_input("index", 5)
    assert engine.input == {"index": 5}

    report = engine.run()
    for fib_type in ["NaiveFibonacci", "IteratorFibonacci", "DpFibonacci"]:
        assert fib_type in report.tasks
        task_report = report.tasks[fib_type]
        assert task_report.output == 8
        assert task_report.metrics["ExecutionTime"]["time"] > 0
