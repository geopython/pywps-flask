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

RUN git clone https://github.com/geopython/pywps-demo.git
 
WORKDIR /pywps-demo
RUN pip3 install -r requirements.txt
 
EXPOSE 5000 
ENTRYPOINT ["/usr/bin/python3", "demo.py","-a"]

#docker build -t pywps-demo . 
#docker run -p 5000:5000 pywps-demo
#http://localhost:5000/wps?request=GetCapabilities&service=WPS
#http://localhost:5000/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0
