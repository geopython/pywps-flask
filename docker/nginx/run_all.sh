#!/bin/bash 
gunicorn -b 127.0.0.1:8081  -D --workers $GU_WORKERS --log-syslog  --pythonpath /pywps-demo wsgi.pywps_app:application
nginx -g 'daemon off;'