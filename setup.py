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
    version='0.2.1',
    py_modules=['cryptosteganography'],
    description='A python steganography module to store messages or files protected with AES-256 encryption inside an image.',
    long_description=readme(),
    url='https://github.com/computationalcore/cryptosteganography',
    author='Vin Busquet',
    author_email='computationalcore@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Security',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['steganography', 'cryptography', 'encryption', 'aes', 'cryptosteganography', 'image'],
    install_requires=install_requires,
    python_requires='>=3',
    entry_points={
        'console_scripts': ['cryptosteganography=cryptosteganography:main'],
    }
)