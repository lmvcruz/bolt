import unittest

from bolt.parameter import Parameter


class ParameterTest(unittest.TestCase):
    def test_create_empty_parameter(self):
        self.assertEqual(Parameter(), {})

    def test_create_parameter_from_dict(self):
        par = Parameter({
            "name": "foo",
            "first_att": "baa",
            "second_att": 5
        })
        self.assertEqual(par, {
            "name": "foo",
            "first_att": "baa",
            "second_att": 5
        })
        self.assertEqual(par.name, "foo")
        self.assertEqual(par.first_att, "baa")
        self.assertEqual(par.second_att, 5)

    def test_attributes_injection(self):
        par = Parameter({
            "name": "fee",
            "first_att": ["zoo"],
            "second_att": 5.9
        })
        self.assertEqual(par.name, "fee")
        self.assertEqual(par.first_att, ["zoo"])
        self.assertEqual(par.second_att, 5.9)

    def test_check_attributes_existence(self):
        par = Parameter({
            "name": "foo",
            "first_att": "baa",
            "second_att": 5
        })
        self.assertTrue("name" in par)
        self.assertFalse("third_att" in par)


if __name__ == '__main__':
    unittest.main()
