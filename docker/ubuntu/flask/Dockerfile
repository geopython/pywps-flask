#based on https://hub.docker.com/r/geographica/gdal2/~/dockerfile/
FROM phusion/baseimage:0.9.22
MAINTAINER Jorge S. Mendes de Jesus <jorge.dejesus@geocat.net>

ARG ROOTDIR=/usr/local/ 
ARG GDAL_VERSION=2.2.3 
ARG PROCESSOR_N=8

WORKDIR $ROOTDIR/


RUN apt-get update -y && apt-get install -y \
    software-properties-common \
    python-software-properties \
    python3-software-properties \
    build-essential \
    python-dev \
    python3-dev \
    python-numpy \
    python3-numpy \
    python3-lxml \
    python3-pip \
    libspatialite-dev \
    sqlite3 \
    libpq-dev \
    libxml2-dev \
    libcurl4-gnutls-dev \
    libproj-dev \
    libxml2-dev \
    libxslt-dev \ 
    libgeos-dev \
    libspatialite-dev \
    libxerces-c-dev \
    libexpat1-dev \
    git \
    bash-completion \
    cmake

ADD http://download.osgeo.org/gdal/${GDAL_VERSION}/gdal-${GDAL_VERSION}.tar.gz $ROOTDIR/src/

RUN cd src/ && tar -xvf gdal-${GDAL_VERSION}.tar.gz && cd gdal-${GDAL_VERSION} \
    && LDFLAGS="-s" ./configure --with-python --with-geos --with-spatialite --with-pg --with-curl --with-xerces --with-expat \
    && make -j ${PROCESSOR_N} && make install && ldconfig \
    && cd $ROOTDIR && cd src/gdal-${GDAL_VERSION}/swig/python \
    && python3 setup.py build \
    && python3 setup.py install \
    && cd $ROOTDIR && rm -Rf src/gdal*
    
WORKDIR /
RUN git clone https://github.com/geopython/pywps-flask.git
 
WORKDIR /pywps-flask
RUN pip3 install -r requirements.txt

RUN mkdir /etc/service/pywps4
COPY pywps4_service.sh /etc/service/pywps4/run
RUN chmod +x /etc/service/pywps4/run
 
EXPOSE 5000
ENTRYPOINT ["/usr/bin/python3", "demo.py","-a"]

#docker build -t pywps-flask . 
#docker run -p 5000:5000 pywps-flask
#http://localhost:5000/wps?request=GetCapabilities&service=WPS
#http://localhost:5000/wps?request=DescribeProcess&service=WPS&identifier=all&version=1.0.0    
   	