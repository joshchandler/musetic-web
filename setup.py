import multiprocessing
import re
from setuptools import setup, find_packages

assert multiprocessing


def get_version():
    """
    Extracts the version number from the version.py file
    """
    VERSION_FILE = 'musetic/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name="Musetic",
    version=get_version(),
    description="A social sharing platform for artists and creators",
    long_description=open('README.md').read(),
    url='http://musetic.com',
    author='Joshua Chandler',
    author_email='Joshua Chandler <joshua@musetic.com>',
    keywords='Musetic',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    license='Private',
    install_requires=[
        'Django==1.8.4',
    ],
    tests_require=[
        'psycopg2',
        'django-nose',
        'mock',
    ],
    include_package_data=True,
    zip_safe=False,
)
