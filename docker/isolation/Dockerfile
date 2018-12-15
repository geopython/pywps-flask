FROM alpine:latest
MAINTAINER Jorge S. Mendes de Jesus <jorge.dejesus@geocat.net>

ENV GDAL_VERSION 2.2.0
ENV XERCES_VERSION 3.2.0

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
	linux-headers \
	expat \
	expat-dev


RUN apk --update --no-cache add g++ libstdc++ make swig

# Xerces
RUN wget http://www.apache.org/dist/xerces/c/3/sources/xerces-c-${XERCES_VERSION}.tar.gz -O /tmp/xerces-c-${XERCES_VERSION}.tar.gz && \
    tar xvf /tmp/xerces-c-${XERCES_VERSION}.tar.gz -C /tmp && \
    cd /tmp/xerces-c-${XERCES_VERSION} && \
    ./configure --prefix=/opt/xerces && \
    make -j 4 && \
    make install

# Geos
RUN apk add --no-cache \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    geos \
    geos-dev

# Install GDAL
RUN wget http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz -O /tmp/gdal.tar.gz && \
	tar xzf /tmp/gdal.tar.gz -C /tmp && \
	cd /tmp/gdal-${GDAL_VERSION} && \
	CFLAGS="-g -Wall" LDFLAGS="-s" ./configure --with-expat=yes --with-xerces=/opt/xerces --with-geos=yes \
	&& make -j 4 && make install

RUN cd /tmp/gdal-${GDAL_VERSION}/swig/python \
	&& python3 setup.py build \
	&& python3 setup.py install

RUN git clone https://github.com/lazaa32/pywps-flask.git

WORKDIR /pywps-flask
RUN pip3 install -r requirements.txt


EXPOSE 5000
ENTRYPOINT ["/usr/bin/python3", "demo.py","-a"]

#docker build -t pywps-flask .
#docker run -p 5000:5000 pywps-flask
#http://localhost:5000/wps?request=GetCapabilities&service=WPS
#http://localhost:5000/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0
