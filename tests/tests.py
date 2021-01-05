import unittest


class LogicTests(unittest.TestCase):
    def test_boolean_logic(self):
        """ Test that boolean logic works """

        self.assertTrue(True, "True should be equal to True.")
        self.assertFalse(False, "False should not be equal to True.")
        self.assertNotEqual(True, False, "True should not be equal to False.")

    def test_maths(self):
        """ Test that basic maths work """

        # Test that basic integers work
        self.assertEqual(int(1) + int(1), int(2), "Basic addition failed")
        self.assertNotEqual(int(1) + int(1), int(3), "Basic addition failed")


if __name__ == '__main__':
    unittest.main()
