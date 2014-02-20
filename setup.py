"""
intervals
---------

Python tools for handling intervals (ranges of comparable objects).
"""
from setuptools import setup, find_packages
import sys


PY3 = sys.version_info[0] == 3


extras_require = {
    'test': [
        'pytest==2.2.3',
        'Pygments>=1.2',
        'six>=1.4.1'
    ],
}


setup(
    name='intervals',
    version='0.2.2',
    url='https://github.com/kvesteri/intervals',
    license='BSD',
    author='Konsta Vesterinen',
    author_email='konsta@fastmonkeys.com',
    description=(
        'Python tools for handling intervals (ranges of comparable objects).'
    ),
    long_description=__doc__,
    packages=find_packages('.'),
    py_modules=['intervals'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    dependency_links=[],
    install_requires=[
        'infinity>=0.1.3',
        'total_ordering>=0.1'
        if sys.version_info[0] == 2 and sys.version_info[1] < 7 else ''
    ],
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
