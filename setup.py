#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.md').read()

with open('requirements.txt') as reqs:
    requirements = reqs.read().split()


setup(
    name='pagseguro',
    version='0.3.2',
    description='Pagseguro API v2 wrapper',
    author='Bruno Rocha',
    author_email='rochacbruno@gmail.com',
    url='https://github.com/rochacbruno/python-pagseguro',
    packages=['pagseguro', ],
    package_dir={'pagseguro': 'pagseguro'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    test_suite='tests',
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
    keywords='pagseguro, payment, payments, credit-card'
)
