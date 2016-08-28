try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Implementation of PyWPS-4 server',
    'author': 'Luis de Sousa',
    'url': 'http://pywps.org',
    'download_url': 'https://github.com/geopython/pywps-demo',
    'author_email': 'luis.a.de.sousa@gmail.com',
    'version': '4.0',
    'install_requires': [],
    'packages': ['processes', 'tests'],
    'scripts': ['demo.py'],
    'name': 'pywps-demo'
}

setup(**config)
