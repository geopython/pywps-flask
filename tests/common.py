import lxml.etree as etree
import sys
import urllib
PY2 = sys.version_info[0] == 2

URL = 'http://localhost:5002/wps'

if not PY2:
    import urllib.request

def get_response(url, post_data=None):

    response = None

    if PY2:
        response = urllib.urlopen(url, data=post_data)
    else:
        #if post_data:
        #    post_data = post_data.decode()
        response = urllib.request.urlopen(url, data=post_data)

    return response

def get_schema(url):

    schema = get_response(url)
    xmlschema_doc = etree.parse(schema)
    return etree.XMLSchema(xmlschema_doc)

def validate_file(path, schema):

    body_doc = etree.parse(path)
    schema = get_schema(schema)
    return schema.validate(body_doc)

def validate(url, schema, post_data=None):
    response = get_response(url, post_data)
    info = response.info()
    body = response.read()
    body_doc = etree.fromstring(body)

    schema = get_schema(schema)

    return schema.validate(body_doc)

