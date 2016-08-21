#!/usr/bin/env python3

import os
import psutil
import sys

import flask

from pywps import Service

from processes.sleep import Sleep
from processes.ultimate_question import UltimateQuestion
from processes.centroids import Centroids
from processes.sayhello import SayHello
from processes.feature_count import FeatureCount
from processes.buffer import Buffer
from processes.area import Area
from processes.bboxinout import Box


app = flask.Flask(__name__)

processes = [
    FeatureCount(),
    SayHello(),
    Centroids(),
    UltimateQuestion(),
    Sleep(),
    Buffer(),
    Area(),
    Box()
]

# This is, how you start PyWPS instance
service = Service(processes, ['pywps.cfg'])

@app.route("/")
def hello():
    return """
    Welcome to PyWPS server. For OGC WPS endpoint, go to http://localhost:5000/wps url
    """

@app.route('/wps', methods=['GET', 'POST'])
def wps():

    return service

@app.route('/outputs/'+'<filename>')
def outputfile(filename):
    targetfile = os.path.join('outputs', filename)
    if os.path.isfile(targetfile):
        file_ext = os.path.splitext(targetfile)[1]
        with open(targetfile, mode='rb') as f:
            file_bytes = f.read()
        mime_type = None
        if 'xml' in file_ext:
            mime_type = 'text/xml'
        return flask.Response(file_bytes, content_type=mime_type)
    else:
        flask.abort(404)

@app.route('/static/'+'<filename>')
def staticfile(filename):
    targetfile = os.path.join('static', filename)
    if os.path.isfile(targetfile):
        file_ext = os.path.splitext(targetfile)[1]
        with open(targetfile, mode='rb') as f:
            file_bytes = f.read()
        mime_type = None
        return flask.Response(file_bytes, content_type=mime_type)
    else:
        flask.abort(404)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Script for starting PyWPS demo instance with sample processes",
        epilog="""Do not use demo in production environment. It's intended to be running in test environment only!
        For more documentation, visit http://pywps.org/doc
        """
        )
    parser.add_argument('-d', '--daemon', action='store_true', help="run in daemon mode")
    args = parser.parse_args()

    if args.daemon:
        pid = None
        try:
            pid = os.fork()
        except OSError as e:
             raise Exception("%s [%d]" % (e.strerror, e.errno))

        if (pid == 0):
            os.setsid()
            app.run(threaded=True)
        else:
            os._exit(0)
    else:
        app.run(threaded=True)

