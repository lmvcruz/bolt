# Benchmark programs
from bolt.tests.programs import fib_bench 
from bolt.tests.programs import rootfinder_bench 

# Unit tests: it is necessary import those classes to run unittest.main()
from bolt.tests.program_controller_test import ProgramControllerTest
from bolt.tests.fibonacci_test import FibonacciTest
from bolt.tests.rootfinder_test import RootFinderTest

import unittest

if __name__ == "__main__":
    fib_bench.main()
    rootfinder_bench.main()
    unittest.main()
