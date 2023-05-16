from bolt.task import Task


class Runner:
    def __init__(self, task):
        self.metrics = []
        self.task = task
        self.report = {"Metrics": {}}

    def add_metric(self, metric):
        self.metrics.append(metric)

    def run(self, parameters: dict) -> dict:
        self.setup()
        exec_out = self.task.run(parameters)
        self.report["ExecutionOutput"] = exec_out
        self.teardown()
        return self.report

    def setup(self):
        self.task.setup()
        for m in self.metrics:
            m.setup()

    def teardown(self):
        for m in self.metrics:
            m.teardown(self.report["ExecutionOutput"])
            self.report["Metrics"][m.name] = m.report
        self.task.teardown()
