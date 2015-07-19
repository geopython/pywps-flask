"""Test various processes
"""
import unittest

from tests.common import validate, URL

class SayHello(unittest.TestCase):
    """Test sayhello process
    """

    def setUp(self):

        self.schema_url = 'http://schemas.opengis.net/wps/1.0.0/wpsExecute_response.xsd'


    def test_valid(self):
        "GET Execute request"

        url = URL + '?service=wps&request=execute&identifier=say_hello&version=1.0.0&datainputs=name=ahoj'
        assert validate(url, self.schema_url)

    def test_valid_lineage(self):
        "GET Execute request, lineage=true"

        url = URL + '?service=wps&request=execute&identifier=say_hello&version=1.0.0&datainputs=name=ahoj&lineage=true'
        assert validate(url, self.schema_url)

def load_tests(loader=None, tests=None, pattern=None):
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(SayHello),
    ]
    return unittest.TestSuite(suite_list)
