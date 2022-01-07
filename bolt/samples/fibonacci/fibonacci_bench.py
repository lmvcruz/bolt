from bolt.samples.fibonacci.fib_program import NaiveFibonacci
from bolt.program import ProgramController


def execute_naive_fibonacci(indices):
    prog = NaiveFibonacci()
    controller = ProgramController()
    controller.set_program(prog)
    for inp in indices:
        input = {"index": inp}
        controller.run(input)
        print(controller.to_dict())


def main():
    execute_naive_fibonacci([0, 1, 2, 3, 4, 5, 6, 7, 8])


if __name__ == "__main__":
    main()
