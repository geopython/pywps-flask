#!/bin/sh
gunicorn -b 0.0.0.0:8081 --workers $GU_WORKERS --log-syslog  --pythonpath /pywps-flask wsgi.pywps_app:application