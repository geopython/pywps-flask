import unittest
import lxml.etree as etree
import urllib
import subprocess

import sys
PY2 = sys.version_info[0] == 2

class CapabilitiesTest(unittest.TestCase):

    def setUp(self):

        self.url = "http://localhost:5001/wps?service=wps&request=getcapabilities"
        schema = urllib.urlopen('http://schemas.opengis.net/wps/1.0.0/wpsGetCapabilities_response.xsd')
        schema = None

        if PY2:
            schema = urllib.urlopen('http://schemas.opengis.net/wps/1.0.0/wpsDescribeProcess_response.xsd')
        else:
            schema = urllib.request.urlopen('http://schemas.opengis.net/wps/1.0.0/wpsDescribeProcess_response.xsd')

        xmlschema_doc = etree.parse(schema)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def test_capabilities(self):
        response = urllib.urlopen(self.url)
        response = None
        if PY2:
            response = urllib.urlopen(self.url)
        else:
            response = urllib.request.urlopen(self.url)
        info = response.info()
        body = response.read()
        body_doc = etree.fromstring(body)
        assert self.xmlschema.validate(body_doc)

def load_tests(loader=None, tests=None, pattern=None):
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(CapabilitiesTest),
    ]
    return unittest.TestSuite(suite_list)
