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

import processes.bboxinout

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
    print("Running WPS server at http://localhost:5000/wps")
    app.run(threaded=True)
