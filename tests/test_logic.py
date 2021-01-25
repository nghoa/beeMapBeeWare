import unittest
from app.services.bee_service import doubleTime
from app.services.database import db_import_test

class LogicTests(unittest.TestCase):
    def test_test(self):
        self.assertEqual(4, doubleTime(2))

class DatabaseTests(unittest.TestCase):
    def db_import_unittest(self):
        self.assertTrue(db_import_test())

if __name__ == '__main__':
    unittest.main()
