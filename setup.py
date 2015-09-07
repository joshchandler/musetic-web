# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'musetic/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='Musetic',
    version=get_version(),
    description='A DIGITAL CREATIVE CONTENT MUSEUM',
    long_description=open('README.md').read(),
    url='http://www.musetic.com',
    author='Josh Chandler, Micah Hausler',
    author_email='joshchandler88@gmail.com, hausler.m@gmail.com',
    keywords='Musetic',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    license='Private',
    install_requires=[
        'Django>=1.7',
    ],
    tests_require=[
        'psycopg2',
        'django-nose',
        'mock',
    ],
    include_package_data=True,
    zip_safe=False,
)
