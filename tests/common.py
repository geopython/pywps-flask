import lxml.etree as etree
import sys
import urllib
PY2 = sys.version_info[0] == 2

URL = 'http://localhost:5000/wps'

if not PY2:
    import urllib.request

def get_response(url):

    response = None

    if PY2:
        response = urllib.urlopen(url)
    else:
        response = urllib.request.urlopen(url)

    return response

def get_schema(url):

    schema = get_response(url)
    xmlschema_doc = etree.parse(schema)
    return etree.XMLSchema(xmlschema_doc)

def validate(url, schema):
    response = get_response(url)
    info = response.info()
    body = response.read()
    body_doc = etree.fromstring(body)
    
    schema = get_schema(schema)

    return schema.validate(body_doc)

