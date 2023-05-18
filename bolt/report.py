from dataclasses import dataclass, field


@dataclass
class TaskReport:
    input: dict = field(default_factory=dict)
    output: str = ""
    metrics: dict[str, dict] = field(default_factory=dict)


@dataclass
class SingleExecutionReport:
    input: dict = field(default_factory=dict)
    tasks: dict[str, TaskReport] = field(default_factory=dict)