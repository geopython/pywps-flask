FROM jorgedejesus/pywps4-demo
MAINTAINER Jorge Samuel Mendes de Jesus <jorge.dejesus@geocat.net>

#For Gunicorn
ARG GU_WORKERS=5
ENV GU_WORKERS=${GU_WORKERS}


RUN apk add --update --no-cache nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY pywps.conf /etc/nginx/conf.d/

COPY run_all.sh /run_all.sh

#For nginx.pid    
RUN mkdir -p /run/nginx


#For pywps
RUN pip3 install gunicorn
RUN ln -s /pywps-flask/wsgi/pywps.wsgi  /pywps-flask/wsgi/pywps_app.py

EXPOSE 80
ENTRYPOINT ["/run_all.sh"]

#Build: docker build -t pywps4-demo:nginx .
#Usage: docker run -p 80:80 -it pywps4-demo:nginx
#Usage w/ 10 workers: docker run -e GU_WORKERS=10  -p 80:80 -it pywps4-demo:nginx

