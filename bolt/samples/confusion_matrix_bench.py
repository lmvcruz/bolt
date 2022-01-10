import math
from random import randint, uniform

from bolt import Parameter
from bolt import Program
from bolt.engine import Engine
from bolt.metrics import ExactDictComparisonMetric


class FlexibleVerificationProgram(Program):
    def __init__(self) -> None:
        super().__init__(FlexibleVerificationProgram.__name__)

    def run(self, input: Parameter):
        res = math.fabs(input["value"] - input["expected"]) < 1.0
        return Parameter({"result": res})


class ConstrainedVerificationProgram(Program):
    def __init__(self) -> None:
        super().__init__(ConstrainedVerificationProgram.__name__)

    def run(self, input: Parameter):
        res = math.fabs(input["value"] - input["expected"]) < 0.5
        return Parameter({"result": res})


def overall_confusion_matrix(report):
    comp_rep = {}
    for prog in report.programs_report:
        cases = report.programs_report[prog].cases
        comp_rep[prog] = {
            "true_positive": 0,
            "true_negative": 0,
            "false_positive": 0,
            "false_negative": 0,
        }
        for case in cases:
            actual = case["output"]["result"]
            expected = case["expected"]["result"]
            if expected and actual:
                comp_rep[prog]["true_positive"] += 1
            elif expected and not actual:
                comp_rep[prog]["false_negative"] += 1
            elif actual:  # expected == False
                comp_rep[prog]["false_positive"] += 1
            else:  # expected == False and actual == False
                comp_rep[prog]["true_negative"] += 1
    return comp_rep


def execute_verification(inputs, expected_results):
    engine = Engine()
    engine.add_program(FlexibleVerificationProgram())
    engine.add_program(ConstrainedVerificationProgram())
    engine.add_results_metrics(ExactDictComparisonMetric())
    for inp, expected in zip(inputs, expected_results):
        engine.add_input_and_expected_output(inp, expected)
    engine.run()
    print(overall_confusion_matrix(engine.report))


def main():
    # for each value in orig_db we added a random noise between -1.2 and 1.2
    # The two validators follows the rules:
    # - FlexibleVerificationProgram: difference less than 1.0
    # - ConstrainedVerificationProgram: difference less than 0.5
    # So, it is expected many more false negatives for the constrained version
    # Aditionally, for each case, we added other 3 fake cases, by adding a noise
    # between -10 and 10. So, few cases are expected to be cosidered false positive
    # (only those which noise is between the tolerance range)
    orig_db = {i: randint(0, 100) for i in range(1000)}
    new_db = {k: [v + uniform(-1.2, 1.2)] for (k, v) in orig_db.items()}
    for key in new_db:
        v = new_db[key][0]
        other_values = [v + uniform(-10, 10) for _ in range(3)]
        new_db[key].extend(other_values)

    inputs = []
    expected_results = []
    for key in new_db:
        inputs.append(Parameter({"value": new_db[key][0], "expected": orig_db[key]}))
        expected_results.append(Parameter({"result": True}))
        for v in new_db[key][1:]:
            inputs.append(Parameter({"value": v, "expected": orig_db[key]}))
            expected_results.append(Parameter({"result": False}))
    execute_verification(inputs, expected_results)


if __name__ == "__main__":
    main()
