#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
requirements = ['requests', 'xmltodict', 'arrow']

setup(
    name='pagseguro',
    version='0.2.1',
    description='Pagseguro API v2 wrapper',
    author='Bruno Rocha',
    author_email='rochacbruno@gmail.com',
    url='https://github.com/rochacbruno/python-pagseguro',
    packages=[
        'pagseguro',
    ],
    package_dir={'pagseguro': 'pagseguro'},
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "tests": [
            "flake8", "nose"
        ]
    },
    license='MIT',
    test_suite='runtests',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    keywords='pagseguro, payment, payments, credit-card')
