.. _deployment:

=================================
Deployment to a production server
=================================

.. note:: This text was taken from `official PyWPS documentation <http://pywps.readthedocs.io/en/latest/deployment.html>`_

Deployment on Apache2 httpd server
----------------------------------

First, the WSGI module must be installed and enabled::

    $ sudo apt-get install libapache2-mod-wsgi
    $ sudo a2enmod wsgi

You then can edit your site configuration file
(`/etc/apache2/sites-enabled/yoursite.conf`) and add the following::

        # PyWPS
        WSGIDaemonProcess pywps user=www-data group=www-data processes=2 threads=5
        WSGIScriptAlias /pywps /var/www/pywps/pywps.wsgi

        <Directory /home/jachym/www/htdocs/wps/>
            WSGIScriptReloading On
            WSGIProcessGroup group
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>

.. note:: `WSGIScriptAlias` points to the `pywps.wsgi` script created
        before - it will be available under the url http://localhost/pywps

And of course restart the server::
    
    $ sudo service apache2 restart
