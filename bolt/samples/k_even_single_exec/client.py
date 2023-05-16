from bolt.runner import Runner
from bolt.metric import ExecutionTimeMetric

from bolt.samples.k_even_single_exec.keventask import KEvenSingleExecutionTask

if __name__ == "__main__":
    metric = ExecutionTimeMetric()
    task = KEvenSingleExecutionTask()
    runner = Runner(task)
    runner.add_metric(metric)
    rep = runner.run({"k": 10})
    print(rep)