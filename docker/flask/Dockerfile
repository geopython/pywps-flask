FROM alpine:latest
MAINTAINER Jorge S. Mendes de Jesus <jorge.dejesus@geocat.net>

RUN apk add --no-cache \
	git \
	gcc \
	bash \
	openssh \
	musl-dev  \
	python3 \
        python3-dev \
	libxml2-dev  \
	libxslt-dev \
	linux-headers

RUN git clone https://github.com/geopython/pywps-flask.git
 
WORKDIR /pywps-flask
RUN pip3 install -r requirements.txt
 
EXPOSE 5000 
ENTRYPOINT ["/usr/bin/python3", "demo.py","-a"]

#docker build -t pywps-flask . 
#docker run -p 5000:5000 pywps-flask
#http://localhost:5000/wps?request=GetCapabilities&service=WPS
#http://localhost:5000/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0
