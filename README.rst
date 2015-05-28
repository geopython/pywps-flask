PyWPS-4 demo application
========================

This is a simple demo app written using PyWPS 4. It has been tested with
QGIS 1.8.


Installation
~~~~~~~~~~~~
The app depends on PyWPS and several other libraries that are listed in
``requirements.txt``. You can install them with pip::

    $ pip install -r requirements.txt
    $ pip install -e git+https://github.com/jachym/pywps-4.git@master#egg=pywps-dev

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
~~~~~~~
Simply run the python file::

    $ python demo.py


Issues
~~~~~~
On Windows PyWPS-4 does not support multiprocessing which is used when making
requests storing the response document and updating the status to displaying to the user
the progression of a process.