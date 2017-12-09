FROM nginx:1.13.7-alpine
MAINTAINER Jorge Samuel Mendes de Jesus <jorge.dejesus@geocat.net>

RUN rm /etc/nginx/conf.d/default.conf
COPY pywps.conf /etc/nginx/conf.d/pywps.conf


#Build: docker build -t pywps4:nginx .
#Usage: docker run -p 80:80 -it pywps4:nginx
