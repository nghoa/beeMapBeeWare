import unittest
from ..bee_service import doubleTime

class LogicTests(unittest.TestCase):
    def test_test(self):
        self.assertEqual(4, doubleTime(2))

if __name__ == '__main__':
    unittest.main()
