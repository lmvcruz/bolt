import subprocess

from bolt import Parameter


class Program:
    def __init__(self, name) -> None:
        self.name = name

    def run(self, _: Parameter):
        raise NotImplementedError()


class ExternalProgram(Program):
    def __init__(self, name, exec, timeout=100) -> None:
        super().__init__(name)
        self.executable = exec
        self.timeout = timeout

    def run(self, inp: Parameter):
        str_args = [str(arg) for arg in inp["arguments"]]
        cmd = f"{self.executable} " + " ".join(str_args)
        self.execution_output = subprocess.run(
            cmd,
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=self.timeout,
        )
        return Parameter({"result": self.execution_output.stdout})
