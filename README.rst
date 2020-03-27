Cryptosteganography
===================

.. image:: https://travis-ci.org/computationalcore/cryptosteganography.svg?branch=master
    :target: https://travis-ci.org/computationalcore/cryptosteganography
.. image:: https://codecov.io/github/computationalcore/cryptosteganography/coverage.svg?branch=master
    :target: https://codecov.io/gh/computationalcore/cryptosteganography
.. image:: https://api.codeclimate.com/v1/badges/1f8d04f4badc720d0eda/maintainability
   :target: https://codeclimate.com/github/computationalcore/cryptosteganography/maintainability
.. image:: https://img.shields.io/pypi/v/cryptosteganography.svg
    :target: https://pypi.python.org/pypi/cryptosteganography
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/status/cryptosteganography.svg
    :target: https://pypi.python.org/pypi/cryptosteganography
    :alt: Development Status
.. image:: https://img.shields.io/pypi/pyversions/cryptosteganography.svg
    :target: https://pypi.python.org/pypi/cryptosteganography
    :alt: Python Versions

A python steganography module to store messages or files protected with
AES-256 encryption inside an image.

Steganography is the art of concealing information within different
types of media objects such as images or audio files, in such a way that
no one, apart from the sender and intended recipient, suspects the
existence of the message. By default steganography is a type of security
through obscurity.

Additionally this module also enhance the security of the steganography through data encryption. The data concealed
is encrypted using AES 256 encryption, a popular algorithm used in symmetric key cryptography.

Prerequisites
-------------

`Python 3+ <https://www.python.org/downloads>`_

`pip3 <https://pip.pypa.io/en/stable>`_

(Most Linux systems comes with python 3 installed by default).

Dependencies Installation (Ubuntu)
----------------------------------

.. code:: bash

    $ sudo apt-get install python3-pip

Dependencies Installation (MacOS)
---------------------------------

To install Python3 I recommend use Homebrew package manager

The script will explain what changes it will make and prompt you before
the installation begins.

.. code:: bash

    $ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Edit your ~/.profile to include (if it is not already there)

.. code:: bash

    export PATH=/usr/local/bin:/usr/local/sbin:$PATH

To install Python 3:

.. code:: bash

    $ brew install python3

Installation
------------

To install the package just run

.. code:: bash

    $ pip3 install cryptosteganography

Usage
-----

Use as a library in a python program
''''''''''''''''''''''''''''''''''''

**Store a message string inside an image**

.. code:: python

    from cryptosteganography import CryptoSteganography

    crypto_steganography = CryptoSteganography('My secret password key')

    # Save the encrypted file inside the image
    crypto_steganography.hide('input_image_name.jpg', 'output_image_file.png', 'My secret message')

    secret = crypto_steganography.retrieve('output_image_file.png')

    print(secret)
    # My secret message

**Store a binary file inside an image**

Note: This only works if the concealed file size is smaller than the input image

.. code:: python

    from cryptosteganography import CryptoSteganography

    message = None
    with open('sample.mp3', "rb") as f:
        message = f.read()

    crypto_steganography = CryptoSteganography('My secret password key')

    # Save the encrypted file inside the image
    crypto_steganography.hide('input_image_name.jpg', 'output_image_file.png', message)

    # Retrieve the file ( the previous crypto_steganography instance could be used but I instantiate a brand new object
    # with the same password key just to demonstrate that can it can be used to decrypt)
    crypto_steganography = CryptoSteganography('My secret password key')
    decrypted_bin = crypto_steganography.retrieve('output_image_file.png')

    # Save the data to a new file
    with open('decrypted_sample.mp3', 'wb') as f:
        f.write(secret_bin)

Use as a python program
'''''''''''''''''''''''

**Check help at command line prompt to learn how to use it.**

.. code:: bash

    $ cryptosteganography -h
    usage: cryptosteganography [-h] {save,retrieve} ...

    A python steganography script that save/retrieve a text/file (AES 256
    encrypted) inside an image.

    positional arguments:
      {save,retrieve}  sub-command help
        save           save help
        retrieve       retrieve help

    optional arguments:
      -h, --help       show this help message and exit

**Save sub command help**

.. code:: bash

    $ cryptosteganography save -h
    usage: cryptosteganography save [-h] -i INPUT_IMAGE_FILE
                                  (-m MESSAGE | -f MESSAGE_FILE) -o
                                  OUTPUT_IMAGE_FILE

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT_IMAGE_FILE, --input INPUT_IMAGE_FILE
                            Input image file.
      -m MESSAGE, --message MESSAGE
                            Your secret message to hide (non binary).
      -f MESSAGE_FILE, --file MESSAGE_FILE
                            Your secret to hide (Text or any binary file).
      -o OUTPUT_IMAGE_FILE, --output OUTPUT_IMAGE_FILE
                            Output image containing the secret.

**Retrieve sub command help**

.. code:: bash

    $ cryptosteganography retrieve -h
    usage: cryptosteganography retrieve [-h] -i INPUT_IMAGE_FILE [-o RETRIEVED_FILE]

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT_IMAGE_FILE, --input INPUT_IMAGE_FILE
                            Input image file.
      -o RETRIEVED_FILE, --output RETRIEVED_FILE
                            Output for the binary secret file (Text or any binary
                            file).

**Save message example**

.. code:: bash

    $ cryptosteganography save -i 4824157.png -m "My secret message..." -o output.png
    Enter the key password:
    Output image output.png saved with success

**Retrieve message example**

.. code:: bash

    $ cryptosteganography retrieve -i output.png
    Enter the key password: 
    My secret message...

**Save file example**

.. code:: bash

    $ cryptosteganography save -i input_image_name.jpg -f duck_logo.pem -o output_file.png
    Enter the key password:
    Output image output_file.png saved with success

**Retrieve file example**

.. code:: bash

    $ cryptosteganography retrieve -i output.png -o decrypted_file
    Enter the key password: 
    decrypted_file saved with success

License
-------

This project is licensed under the MIT License - see the
`LICENSE <https://github.com/computationalcore/cryptosteganography/blob/master/LICENSE>`_ file for details


Authors
-------

`Vin Busquet <https://github.com/computationalcore>`_ file for details


Limitations
-----------

-  Only works with python 3
-  It does not work if the conceived file is greater than original input
   file
- Ouput image is limited to PNG format only.
-  I did not tested with all conceived file types. Feel free to
   `report <https://github.com/computationalcore/cryptosteganography/issues>`_ any bug you find


Contributing
------------

For details, check out `CONTRIBUTING.md <https://github.com/computationalcore/cryptosteganography/blob/master/CONTRIBUTING.md>`_.


Changelog
---------

For details, check out `CHANGELOG.md <https://github.com/computationalcore/cryptosteganography/blob/master/CHANGELOG.md>`_.


Acknowledgments
---------------

-  `PyCryptodome <https://github.com/Legrandin/pycryptodome>`_
-  `Stéganô <https://github.com/cedricbonhomme/Stegano>`_
