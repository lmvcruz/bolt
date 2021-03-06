from bolt.program import ProgramController
from bolt.tests.programs.rootfinder import NewtonRootFinder
from bolt.tests.programs.rootfinder import SubdivisionRootFinder


def estimate_root_finder(prog, input):
    controller = ProgramController()
    controller.set_program(prog)
    for case in input["cases"]:
        controller.run(case)
        print(controller.output)
        print(f"Execution time: {controller.execution_time}")


def main():
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
    estimate_root_finder(NewtonRootFinder(), input)
    estimate_root_finder(SubdivisionRootFinder(), input)


if __name__ == "__main__":
    main()
