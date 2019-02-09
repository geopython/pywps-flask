FROM nginx:1.15.7-alpine
MAINTAINER Jorge Samuel Mendes de Jesus <jorge.dejesus@geocat.net>

RUN rm /etc/nginx/conf.d/default.conf
COPY pywps.conf /etc/nginx/conf.d/pywps.conf


#Build: docker build -t pywps/nginx-alpine:latest .
#Usage: docker-compose up
#Usage: docker run -p 80:80 -it pywps/nginx-alpine:latest
