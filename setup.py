#!/usr/bin/env python3

import setuptools


def readme():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()

setuptools.setup(
    name='cryptosteganography',
    version='0.8.4',
    py_modules=['cryptosteganography'],
    description='A python steganography module to store messages or files protected with AES-256 encryption inside an image.',
    long_description=readme(),
    long_description_content_type='text/x-rst',

    url='https://github.com/computationalcore/cryptosteganography',
    author='Vin Busquet',
    author_email='computationalcore@gmail.com',

    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},

    # pip 9.0+ will inspect this field when installing to help users install a
    # compatible version of the library for their Python version.
    python_requires='>=3.9',

    # There are some peculiarities on how to include package data for source
    # distributions using setuptools. You also need to add entries for package
    # data to MANIFEST.in.
    # See https://stackoverflow.com/questions/7522250/
    include_package_data=True,

    # This is a trick to avoid duplicating dependencies between both setup.py and
    # requirements.txt.
    # requirements.txt must be included in MANIFEST.in for this to work.
    # It does not work for all types of dependencies (e.g. VCS dependencies).
    # For VCS dependencies, use pip >= 19 and the PEP 508 syntax.
    #   Example: 'requests @ git+https://github.com/requests/requests.git@branch_or_tag'
    #   See: https://github.com/pypa/pip/issues/6162
    install_requires=[line.strip() for line in open('requirements.txt').readlines()],
    zip_safe=False,

    license='MIT',
    license_files=['LICENSE'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],

    entry_points={
        'console_scripts': ['cryptosteganography=cryptosteganography.cli:main'],
    }
)
