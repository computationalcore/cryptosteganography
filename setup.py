#! coding: utf-8
import sys
from setuptools import setup

py_version = sys.version_info[:2]

# All versions
install_requires = [
    'setuptools',
    'pycryptodomex',
    'Stegano'
]

if py_version < (3, 2):
    install_requires += [
        'futures',
    ]


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='cryptosteganography',
    version='0.2.0',
    py_modules=['cryptosteganography'],
    description='A python steganography module to store messages or files protected with AES-256 encryption inside an image.',
    long_description=readme(),
    url='https://github.com/computationalcore/cryptosteganography',
    author_email='computationalcore@gmail.com',
    license='MIT'
)