#based on https://hub.docker.com/r/geographica/gdal2/~/dockerfile/
#Using a fat docker since other images like nginx-gunicorn will just incorporate extra services
FROM phusion/baseimage:0.11
MAINTAINER Jorge S. Mendes de Jesus <jorge.dejesus@protomail.com>

ARG ROOTDIR=/usr/local/ 
ARG GDAL_VERSION=2.4.0
ARG PROCESSOR_N=8
ARG FLASK_GIT=https://github.com/jorgejesus/pywps-flask.git
ARG FLASK_BRANCH=pywps_4.2

WORKDIR $ROOTDIR/

RUN apt-get update -y && install_clean \
	software-properties-common \
	build-essential \
	python3-dev \
	python3-numpy \
	python3-lxml \
	python3-lxml \
	python3-pip \
	python3-wheel \
	python3-setuptools \
	libspatialite-dev \
	sqlite3 \
	libpq-dev \
	libxml2-dev \
	libcurl4-gnutls-dev \
	libproj-dev \
	libxml2-dev \
	libxslt-dev \
	libgeos-dev \ 
	libxerces-c-dev \
	git \
	cmake


ADD http://download.osgeo.org/gdal/$GDAL_VERSION/gdal-$GDAL_VERSION.tar.gz $ROOTDIR/src/

RUN cd src/ && tar -xvf gdal-$GDAL_VERSION.tar.gz && cd gdal-$GDAL_VERSION \
    && LDFLAGS="-s" ./configure --with-python --with-geos --with-spatialite --with-pg --with-curl --with-xerces --with-expat \
    && make -j $PROCESSOR_N && make install && ldconfig \
    && cd $ROOTDIR && cd src/gdal-$GDAL_VERSION/swig/python \
    && python3 setup.py build \
    && python3 setup.py install \
    && cd $ROOTDIR && rm -Rf src/gdal*

    
WORKDIR /
RUN git clone $FLASK_GIT -b $FLASK_BRANCH --single-branch 
 
WORKDIR /pywps-flask
RUN pip3 install -r requirements.txt

RUN mkdir /etc/service/pywps4
COPY pywps4_service.sh /etc/service/pywps4/run
RUN chmod +x /etc/service/pywps4/run
 
 
EXPOSE 5000

#docker build -t pywps/flask-ubuntu:latest . 
#docker run -p 5000:5000 pywps/flask-ubuntu
#http://localhost:5000/wps?request=GetCapabilities&service=WPS
#http://localhost:5000/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0    
   	