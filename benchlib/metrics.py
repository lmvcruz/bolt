from benchlib.parameter import Parameter


class Metric:
    def __init__(self) -> None:
        self.result = None
    
    def evaluate(self, output: Parameter):
        return self.result

class EmptyMetric(Metric):
    def __init__(self) -> None:
        super().__init__()

    def evaluate(self, output: Parameter):
        self.result = output is None
        return self.result
