from bolt.samples.keventask import KEvenSingleExecutionTask


def test_keven_task():
    # This task is just a sample to be used for tests and demo
    task = KEvenSingleExecutionTask()
    assert task.run({"k": 3}) == "0 2 4"
