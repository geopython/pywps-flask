try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Implementation of PyWPS-4 server',
    'author': 'Luis de Sausa',
    'url': 'http://pywps.org',
    'download_url': 'https://github.com/ldesousa/pywps-4-demo',
    'author_email': 'luis.a.de.sousa@gmail.com',
    'version': '4.0',
    'install_requires': [],
    'packages': ['processes', 'tests'],
    'scripts': ['demo.py'],
    'name': 'pywps-4-demo'
}

setup(**config)
