import sys


def naive_fib(n: int) -> int:
    if n < 2:
        return 1
    return naive_fib(n - 1) + naive_fib(n - 2)


def internal_dp_fib(n, memo):
    if n < 2:
        return 1
    if n in memo:
        return memo[n]
    n1 = memo[n - 1] if n - 1 in memo else internal_dp_fib(n - 1, memo)
    n2 = memo[n - 2] if n - 2 in memo else internal_dp_fib(n - 2, memo)
    memo[n] = n1 + n2
    return memo[n]


def dp_fib(n):
    memo = {}
    return internal_dp_fib(n, memo)


def iterator_fib(n):
    if n < 2:
        return 1
    n1 = 1
    n2 = 1
    fib = n1 + n2
    for _ in range(n + 1)[3:]:
        n1 = n2
        n2 = fib
        fib = n1 + n2
    return fib


def main():
    if len(sys.argv) != 3:
        print("ERROR")
        return

    # Arguments are strings and then must be converted to be internally
    # used as int values
    fib_index = int(sys.argv[1])
    fib_type = sys.argv[2]
    if fib_type == "NAIVE":
        print(naive_fib(fib_index))
    elif fib_type == "DP":
        print(dp_fib(fib_index))
    elif fib_type == "ITERATOR":
        print(iterator_fib(fib_index))
    else:
        print("ERROR")


if __name__ == "__main__":
    main()
