import os
import sys
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(ROOT_DIR)

# Benchmark programs
from bolttests.programs import fib_bench 
from bolttests.programs import rootfinder_bench 

# Unit tests: it is necessary import those classes to run unittest.main()
from bolttests.program_controller_test import ProgramControllerTest
from bolttests.fibonacci_test import FibonacciTest
from bolttests.rootfinder_test import RootFinderTest

import unittest

if __name__ == "__main__":
    fib_bench.main()
    rootfinder_bench.main()
    unittest.main()
