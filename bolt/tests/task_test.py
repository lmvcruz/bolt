from bolt.samples.k_even_single_exec.keventask import KEvenSingleExecutionTask

# This task is just a sample to be used for tests and demo
def test_keven_task():
    task = KEvenSingleExecutionTask()
    assert task.run({"k": 3}) == "0 2 4"