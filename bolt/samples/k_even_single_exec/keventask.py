from bolt.task import Task


class KEvenSingleExecutionTask(Task):
    def __init__(self) -> None:
        super().__init__()

    def run(self, parameters: dict) -> str:
        return ' '.join([str(i*2) for i in range(int(parameters["k"]))])