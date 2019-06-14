# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fr:
    required = fr.read().splitlines()

setup(
    name='alice_wsgi',
    version='0.0.5',
    packages=['alice_wsgi', ],
    url='https://github.com/ndrwpvlv/mimemiko',
    license='',
    author='Andrei S. Pavlov',
    author_email='ndrw.pvlv@gmail.com',
    description='alice_wsgi - wsgi micro framework with class based views and modular system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
)
