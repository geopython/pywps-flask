import unittest
import sqlite3

class LoggingTest(unittest.TestCase):

    def test_db_log(self):

        conn = sqlite3.connect('logs/pywps-logs.sqlite3')

        cur = conn.cursor()
        cur.execute('select * from pywps_stored_requests')
        all_lines = cur.fetchall()

        self.assertEqual(len(all_lines)%5, 0)

def load_tests(loader=None, tests=None, pattern=None):
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(LoggingTest),
    ]
    return unittest.TestSuite(suite_list)
