from dataclasses import dataclass, field

# @dataclass
# class MetricTaskExecutionReport:
#     name: str = ""
#     value: dict = field(default_factory=dict)


@dataclass
class TaskReport:
    # task_name: str = ""
    input: dict = field(default_factory=dict)
    output: str = ""
    metrics: dict[str, dict] = field(default_factory=dict)

@dataclass
class SingleExecutionReport:
    input: dict = field(default_factory=dict)
    tasks: dict[str, TaskReport] = field(default_factory=dict)