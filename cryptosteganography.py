# -*- coding: utf-8 -*-

"""
A python steganography module to store messages and files AES-256 encrypted inside an image.
"""

from __future__ import print_function

__author__ = 'computationalcore@gmail.com'

import argparse
import base64
import hashlib
import getpass
import pkg_resources
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome import Random
from stegano import lsb, tools


class CryptoSteganography(object):
    """
    Main class to handle Steganography encrypted data.
    """

    def __init__(self, key):
        """
        Constructor
        :param key: string that used to derive the key
        """
        self.block_size = 32
        # Create a sha256 hash from the informed string key
        self.key = hashlib.sha256(key.encode()).digest()

    def hide(self, input_filename, output_filename, data):
        """
        Encrypt and save the data inside the image.
        :param input_filename: Input image file path
        :param output_filename: Output image file path
        :param data: Information to be encrypted and saved
        :return:
        """
        # Generate a random initialization vector
        iv = Random.new().read(AES.block_size)
        encryption_suite = AES.new(self.key, AES.MODE_CBC, iv)

        # If it is string convert to byte string before use it
        if isinstance(data, str):
            data = data.encode()

        # Encrypt the random initialization vector concatenated with the padded data
        cypher_data = encryption_suite.encrypt(iv + pad(data, self.block_size))

        # Convert the cypher byte string to a base64 string to avoid decode padding error
        cypher_data = base64.b64encode(cypher_data).decode()

        # Hide the encrypted message in the image with the LSB (Least Significant Bit) technique.
        secret = lsb.hide(input_filename, cypher_data)
        # Save the image file
        secret.save(output_filename)

    def retrieve(self, input_image_file):
        """
        Retrieve the encrypted data from the image.
        :param input_image_file: Input image file path
        :return:
        """
        cypher_data = lsb.reveal(input_image_file)

        if not cypher_data:
            return None

        cypher_data = base64.b64decode(cypher_data)
        # Retrieve the dynamic initialization vector saved
        iv = cypher_data[:AES.block_size]
        # Retrieved the cypher data
        cypher_data = cypher_data[AES.block_size:]

        try:
            decryption_suite = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = unpad(decryption_suite.decrypt(cypher_data), self.block_size)
            try:
                return decrypted_data.decode('utf-8')
            except UnicodeDecodeError:
                # Binary data - returns as it is
                return decrypted_data
        except ValueError:
            return None


def main():
    """
    Run Script
    :return:
    """

    parser = argparse.ArgumentParser(
        prog='cryptosteganography',
        description="Cryptosteganography is an application to save or retrieve an encrypted message or encrypted file concealed inside an image."
    )

    parser.add_argument("-v", "--version", action='version', version=pkg_resources.require("cryptosteganography")[0].version)

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    # Sub parser: Save
    parser_save = subparsers.add_parser('save', help='save help')
    # Original image
    parser_save.add_argument("-i", "--input", dest="input_image_file",
                             required=True, help="Input image file.")

    group_secret = parser_save.add_mutually_exclusive_group(required=True)
    # Non binary secret message to hide
    group_secret.add_argument("-m",  "--message", dest="message",
                              help="Your secret message to hide (non binary).")
    # Binary secret message to hide
    group_secret.add_argument("-f",  "--file", dest="message_file",
                              help="Your secret to hide (Text or any binary file).")

    # Image containing the secret
    parser_save.add_argument("-o", "--output", dest="output_image_file",
                             required=True, help="Output image containing the secret.")

    # Sub parser: Retrieve
    parser_retrieve = subparsers.add_parser('retrieve', help='retrieve help')
    parser_retrieve.add_argument("-i", "--input", dest="input_image_file",
                               required=True, help="Input image file.")
    parser_retrieve.add_argument("-o", "--output", dest="retrieved_file",
                               help="Output for the binary secret file (Text or any binary file).")

    args = parser.parse_args()

    # Save action
    if args.command == 'save':

        message = ''
        if args.message:
            message = args.message
        elif args.message_file:
            try:
                with open(args.message_file, "r", encoding='utf-8') as f:
                    message = f.read()
            except Exception as error:
                try:
                    # Try to read as binary if failed as utf-8 encoded string based file
                    with open(args.message_file, "rb") as f:
                        message = f.read()
                except Exception as error:
                    # Failed in general
                    print('Error while reading reading input')
                    print(error)
                    exit(0)
            if message == '':
                print('Failed: File content can\'t be empty')
                exit(0)

        # Validate message
        if message == '':
            print('Failed: Message can\'t be empty')
            exit(0)

        # Get password (the string used to derivate the encryption key)
        password = ''
        while True:
            password = getpass.getpass(prompt='Enter the key password: ')
            if len(password) > 0:
                break
            print('Password can\'t be empty')

        password_confirmation = ''
        password_confirmation = getpass.getpass(prompt='Confirm the key password: ')
        if password_confirmation != password:
            print('Failed: Password Confirmation doesn\'t match Password')
            exit(0)

        # Validate password value
        crypto_steganography = None
        try:
            crypto_steganography = CryptoSteganography(password)
        except Exception as error:
            print('Invalid key password format')
            print(error)
            exit(0)

        output_image_file = args.output_image_file
        if not output_image_file:
            output_image_file = 'output.png'
        else:
            # If output image doesn't have png suffix or is in other format, force png append
            if output_image_file[-4:].lower() != '.png':
                output_image_file += '.png'

        # Hide and save the image
        try:
            crypto_steganography.hide(args.input_image_file, output_image_file, message)
        except Exception as error:
            print('Error while saving data')
            print(error)
            exit(0)

        print('Output image %s saved with success' % output_image_file)

    # Retrieve action
    elif args.command == 'retrieve':
        # Get password (the string used to derive the encryption key)
        password = ''
        while True:
            password = getpass.getpass('Enter the key password: ')
            if len(password) > 0:
                break
            print('Password can\'t be empty')

        crypto_steganography = CryptoSteganography(password)

        secret = crypto_steganography.retrieve(args.input_image_file)

        if not secret:
            print('No valid data found')
            exit(0)

        # Print or save to a file the data
        if args.retrieved_file:
            try:
                with open(args.retrieved_file, 'wb') as f:
                    f.write(secret)
            except TypeError:
                try:
                    with open(args.retrieved_file, 'wb') as f:
                        f.write(secret.encode())
                except Exception as error:
                    print('Error while saving output file')
                    print(error)
                    exit(0)
            print('%s saved with success' % args.retrieved_file)
        else:
            print(secret)
    # Print help
    else:
        parser.print_help()



if __name__ == '__main__':
    main()
