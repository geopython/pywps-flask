import unittest
import lxml.etree as etree
import urllib
import subprocess

from tests.common import validate, URL

class SayHello(unittest.TestCase):

    def setUp(self):

        self.url = URL + '?service=wps&request=execute&identifier=say_hello&version=1.0.0&datainputs=name=ahoj'
        self.schema_url = 'http://schemas.opengis.net/wps/1.0.0/wpsExecute_response.xsd'


    def test_valid(self):

        assert validate(self.url, self.schema_url)

def load_tests(loader=None, tests=None, pattern=None):
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(SayHello),
    ]
    return unittest.TestSuite(suite_list)
