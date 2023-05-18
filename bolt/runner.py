from bolt.task import Task
from bolt.report import TaskReport


class Runner:
    def __init__(self, task: Task):
        self.metrics = []
        self.task = task
        self.report = TaskReport()

    @property
    def name(self):
        return self.task.name

    def add_metric(self, metric):
        self.metrics.append(metric)

    def run(self, input: dict) -> TaskReport:
        self.setup()
        self.report.input = input
        self.report.output = self.task.run(input)
        self.teardown()
        return self.report

    def setup(self):
        self.task.setup()
        for m in self.metrics:
            m.setup()

    def teardown(self):
        for m in self.metrics:
            m.teardown(self.report.output)
            self.report.metrics[m.name] = m.report
        self.task.teardown()
