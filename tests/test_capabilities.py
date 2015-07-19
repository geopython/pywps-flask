import unittest
import lxml.etree as etree
import urllib
import subprocess

from tests.common import validate, URL

class CapabilitiesTest(unittest.TestCase):

    def setUp(self):

        self.url = URL + "?service=wps&request=getcapabilities"
        self.schema_url = 'http://schemas.opengis.net/wps/1.0.0/wpsGetCapabilities_response.xsd'

    def test_valid(self):
        assert validate(self.url, self.schema_url)

def load_tests(loader=None, tests=None, pattern=None):
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(CapabilitiesTest),
    ]
    return unittest.TestSuite(suite_list)
