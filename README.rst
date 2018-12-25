PyWPS demo with docker support
==============================
Clone pywps-flask, install libraries, build docker image (due to GDAL compiling lasts quite long)::

    $ pip3 install -r requirements.txt
    $ cd pywps-flask/docker/alpine/flask
    $ docker build -t pywps_container .


Clone pywps and OWSLib::

    $ git clone https://github.com/lazaa32/pywps.git
    $ git clone https://github.com/lazaa32/OWSLib.git

Set PYTHONPATH::

    $ export PYTHONPATH=$PYTHONPATH:$PWD/OWSLib:$PWD/pywps

Run server::

    python3 demo.py


PyWPS example service
========================

This is a simple example service written using PyWPS. It has been tested with
QGIS 1.8.


Installation
------------
The app depends on PyWPS and several other libraries that are listed in
``requirements.txt``. You can install them with pip::

    $ pip install -r requirements.txt

For Debian based systems you will need to install GDAL with::

    $ sudo apt-get install python-gdal

For Windows systems install you need to install Shapely and GDAL by using Python Wheels.
If you have Shapely already installed you might have to uninstall it and installed as a Wheel for it to work::

    Download the corresponding wheel for Shapely: http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely

    Download the corresponding wheel for GDAL: http://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

    $ pip install wheel

    $ pip install Shapely?x.x.x?cpxx?none?win_xxx.whl

    $ pip install GDAL?x.x.x?cpxx?none?win_xxx.whl


Running
-------
Simply run the python file::

    $ python demo.py


Docker
------
The docker folder contains 2 subfolders, each subfolder contains a differente pywps implementation. Folder ``flask`` 
has the default pywps-flask implementation using only Flask while folder ``nginx``  implements pywps using Nginx and Green unicorn as WSGI server.


Docker-flask
------------

To build the image (inside the folder with the Dockerfile):: 

    $ docker build -t pywps4-demo:latest .

And to run it:: 

    $ docker run -p 5000:5000 pywps4-demo:latest


Pywps will be available in  the following URL::

    $ http://localhost:5000 


Docker-nginx
------------

To build the image (inside the folder with the Dockerfile)::

    $ docker build -t pywps4-demo .


Gunicorn uses a set of workers to run pywps (normally ``workers = (2 * cpu) + 1``), the default value used was 5 but it can be overwritten by setting the env flag GU_WORKERS:: 


    $ docker run -e GU_WORKERS=10  -p 80:80 -it pywps4-demo:nginx


In this case pywps (only the WPS) will be avalable on::


    http://localhost

(testing trigger)







