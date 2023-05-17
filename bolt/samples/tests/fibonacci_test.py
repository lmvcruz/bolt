from bolt.samples.fibonacci import NaiveFibonacci, DpFibonacci, IteratorFibonacci

def test_naive_fib():
    fib = NaiveFibonacci()
    assert fib.run({"index": 4}) == 5
    assert fib.run({"index": 5}) == 8
    assert fib.run({"index": 6}) == 13

def test_dp_fib():
    fib = DpFibonacci()
    assert fib.run({"index": 4}) == 5
    assert fib.run({"index": 5}) == 8
    assert fib.run({"index": 6}) == 13

def test_iterator_fib():
    fib = IteratorFibonacci()
    assert fib.run({"index": 4}) == 5
    assert fib.run({"index": 5}) == 8
    assert fib.run({"index": 6}) == 13