#!/bin/bash 
gunicorn -b 0.0.0.0:$GU_PORT --workers $GU_WORKERS --log-syslog  --pythonpath /pywps-flask wsgi.pywps_app:application