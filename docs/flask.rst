.. _flask:

====================
Flask microframework
====================

`Flask <http://flask.pocoo.org>`_ microframework is among others

* built-in development server and debugger
* RESTful request dispatching
* 100% WSGI 1.0 compliant

That means, that you can develop your PyWPS application and modules using Flask
server and then move it to production environment (e.g. with Apache2 HTTP
server).

Start PyWPS server
------------------

For starting the server, just call::

    $ python3 demo.py
    
You should be noticed about Running WPS server at http://localhost:5000/wps

Testing the server
------------------

You should be able to interact with the server just like it would be any other
server, either putting the requests to the web browser or using e.g. `wget`::

    $ wget --content-on-error -O - "http://localhost:5000/wps?service=wps&request=getcapabilities"

Or visit the URL directly in the browser:

    http://localhost:5000/wps?service=wps&request=getcapabilities

You should see the response::

     <!-- PyWPS 4.0.0-alpha2 -->
     <wps:Capabilities xmlns:ows="http://www.opengis.net/ows/1.1"
     ...
     </wps:Capabilities>

If do do anything wrong, you should see the result in Flask terminal::

    http://localhost:5000/wps

With response::

        <?xml version="1.0" encoding="UTF-8"?>
        <!-- PyWPS 4.0.0-alpha2 -->
        <ows:ExceptionReport .... >
        <ows:Exception exceptionCode="MissingParameterValue" locator="service" >
            <ows:ExceptionText>service</ows:ExceptionText>
        </ows:Exception>
    
And output from Flask in the terminal::

        ERROR:PYWPS:Exception: code: 400, locator: service, description: service
        NoneType
