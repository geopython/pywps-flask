#based on https://hub.docker.com/r/geographica/gdal2/~/dockerfile/
FROM pywps/flask-ubuntu:16.0.4
MAINTAINER Jorge S. Mendes de Jesus <jorge.dejesus@geocat.net>

#For Gunicorn
ARG GU_WORKERS=5
ENV GU_WORKERS=${GU_WORKERS}
 
RUN apt-get update -y && apt-get install -y \
	nginx

RUN rm /etc/nginx/sites-enabled/default
COPY pywps.conf /etc/nginx/sites-enabled/pywps.conf
 
WORKDIR /pywps-flask
RUN pip3 install gunicorn
RUN ln -s /pywps-flask/wsgi/pywps.wsgi  /pywps-flask/wsgi/pywps_app.py



COPY pywps4_service.sh /etc/service/pywps4/run
RUN chmod +x /etc/service/pywps4/run

RUN mkdir /etc/service/nginx
COPY nginx_service.sh /etc/service/nginx/run
RUN chmod +x /etc/service/nginx/run

EXPOSE 80
 
#EXPOSE 5000
#ENTRYPOINT ["/usr/bin/python3", "demo.py","-a"]

#docker build -t pywps-flask . 
#docker run -p 5000:5000 pywps-flask
#http://localhost:5000/wps?request=GetCapabilities&service=WPS
#http://localhost:5000/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0    
   	