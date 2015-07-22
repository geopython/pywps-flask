"""Test various processes
"""
import unittest

from tests.common import validate, URL, get_response

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

class Buffer(unittest.TestCase):
    """Test buffer process
    """

    def setUp(self):

        self.schema_url = 'http://schemas.opengis.net/wps/1.0.0/wpsExecute_response.xsd'
        self.url = URL
        resp = get_response('http://localhost:5000/static/requests/execute_buffer_post.xml')
        self.request_data = resp.read()

    def test_valid(self):
        "POST Execute request"

        assert validate(self.url, self.schema_url, self.request_data)

    #def test_valid_lineage(self):
    #    "GET Execute Buffer"

    #    assert validate(url, self.schema_url)

def load_tests(loader=None, tests=None, pattern=None):
    if not loader:
        loader = unittest.TestLoader()
    suite_list = [
        loader.loadTestsFromTestCase(SayHello),
        loader.loadTestsFromTestCase(Buffer)
    ]
    return unittest.TestSuite(suite_list)
