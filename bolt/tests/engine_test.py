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

    assert engine.report == {}
    engine.run()
    # assert "NaiveFibonacci" in engine.report
    # assert "IteratorFibonacci" in engine.report
    # assert "DpFibonacci" in engine.report

