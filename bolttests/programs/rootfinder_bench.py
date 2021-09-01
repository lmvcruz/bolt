import os
import sys
ROOT_DIR = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(ROOT_DIR)

from benchlib.engine import Engine
from bolttests.programs.rootfinder import NewtonRootFinder, SubdivisionRootFinder


def estimateRootFinder(prog, input):
    engine = Engine()
    engine.setProgram(prog)
    for case in input["cases"]:
        engine.run(case)
        print(engine.output)
        print(f"Execution time: {engine.execution_time}")


if __name__ == "__main__":
    input = {
        "cases": [
            {
                "init": 1,
                "end": 3,
                "func": "lambda x: math.pow(x-0.0001, 2) - 3.2"
            },
            {
                "init": 0,
                "end": 3,
                "func": "lambda x: math.sin(x-1)"
            },
            {
                "init": 0,
                "end": 2,
                "func": "lambda x: math.tan(x-1)"
            },
            {
                "init": -3.5,
                "end": -1,
                "func": "lambda x: math.pow(math.exp(x-1), 2) - math.tan(x-1)"
            },
        ]
    }
    estimateRootFinder(NewtonRootFinder(), input)
    estimateRootFinder(SubdivisionRootFinder(), input)
