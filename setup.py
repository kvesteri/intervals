"""
intervals
---------

Python tools for handling intervals (ranges of comparable objects).
"""
from setuptools import setup
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY3 = sys.version_info[0] == 3


def get_version():
    filename = os.path.join(HERE, 'intervals', '__init__.py')
    with open(filename) as f:
        contents = f.read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)


extras_require = {
    'test': [
        'pytest>=2.2.3',
        'Pygments>=1.2',
        'flake8>=2.4.0',
        'isort>=4.2.2',
    ],
}


setup(
    name='intervals',
    version=get_version(),
    url='https://github.com/kvesteri/intervals',
    license='BSD',
    author='Konsta Vesterinen',
    author_email='konsta@fastmonkeys.com',
    description=(
        'Python tools for handling intervals (ranges of comparable objects).'
    ),
    long_description=__doc__,
    packages=['intervals'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    dependency_links=[],
    install_requires=[
        'infinity>=0.1.3',
    ],
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
