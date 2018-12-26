FROM pywps/flask-alpine:latest
MAINTAINER Jorge Samuel Mendes de Jesus <jorge.dejesus@protonmail.com>

#For Gunicorn
ARG GU_WORKERS=5
ENV GU_WORKERS=${GU_WORKERS}
ARG GU_PORT=8081
ENV GU_PORT=${GU_PORT}


COPY run_all.sh /run_all.sh

#For pywps
RUN pip3 install gunicorn
RUN ln -s /pywps-flask/wsgi/pywps.wsgi  /pywps-flask/wsgi/pywps_app.py


ENTRYPOINT ["/run_all.sh"]

#Build: docker build -t pywps/gunicorn-alpine:latest .
#Usage: docker run -p 8081:8081 -it pywps/gunicorn-alpine:latest
#Usage w/ 10 workers: docker run -e GU_WORKERS=10 -e GU_PORT=8082  -p 8082:8082 -it pywps/gunicorn-alpine:latest

