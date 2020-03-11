# -*- coding: utf-8 -*-

"""
A python steganography module to store messages and files AES-256 encrypted
inside an image.
"""
import argparse
import getpass
import sys

from exitstatus import ExitStatus
import pkg_resources

from cryptosteganography import CryptoSteganography

__author__ = 'computationalcore@gmail.com'


def parse_args(parse_this=None) -> argparse.Namespace:
    """Parse user command line arguments."""
    parser = argparse.ArgumentParser(
        prog='cryptosteganography',
        description="""
            Cryptosteganography is an application to save or retrieve
            an encrypted message or encrypted file concealed inside an image.
        """
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=pkg_resources.require('cryptosteganography')[0].version
    )

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    # Sub parser: Save
    parser_save = subparsers.add_parser(
        'save',
        help='save help'
    )
    # Original image
    parser_save.add_argument(
        '-i',
        '--input',
        dest='input_image_file',
        required=True,
        help='Input image file.'
    )

    group_secret = parser_save.add_mutually_exclusive_group(required=True)
    # Non binary secret message to hide
    group_secret.add_argument(
        '-m',
        '--message',
        dest='message',
        help='Your secret message to hide (non binary).'
    )
    # Binary secret message to hide
    group_secret.add_argument(
        '-f',
        '--file',
        dest='message_file',
        help='Your secret to hide (Text or any binary file).'
    )

    # Image containing the secret
    parser_save.add_argument(
        '-o',
        '--output',
        dest='output_image_file',
        required=True,
        help='Output image containing the secret.'
    )

    # Sub parser: Retrieve
    parser_retrieve = subparsers.add_parser(
        'retrieve',
        help='retrieve help'
    )
    parser_retrieve.add_argument(
        '-i',
        '--input',
        dest='input_image_file',
        required=True,
        help='Input image file.'
    )
    parser_retrieve.add_argument(
        '-o',
        '--output',
        dest='retrieved_file',
        help='Output for the binary secret file (Text or any binary file).'
    )

    return parser.parse_args(parse_this)


def main() -> ExitStatus:
    """
    Accept arguments and run the script.

    :return:
    """
    args = parse_args()

    # Save action
    if args.command == 'save':

        message = b''
        if args.message:
            message = args.message
        elif args.message_file:
            try:
                with open(args.message_file, 'rb', encoding='utf-8') as f:
                    message = f.read()
            except Exception:
                try:
                    # Try to read as binary if failed as utf-8 encoded string based file
                    with open(args.message_file, 'rb') as f:
                        message = f.read()
                except FileNotFoundError:
                    print('Failed: Message file %s not found.' % args.message_file)
                    return ExitStatus.failure
            if message == b'':
                print("Failed: Message file content can't be empty")
                return ExitStatus.failure

        # Validate message
        if not message:
            print("Failed: Message can't be empty")
            return ExitStatus.failure

        # Get password (the string used to derivate the encryption key)
        password = getpass.getpass('Enter the key password: ').strip()
        if len(password) == 0:
            print("Failed: Password can't be empty")
            return ExitStatus.failure

        password_confirmation = ''
        password_confirmation = getpass.getpass(prompt='Confirm the key password: ').strip()
        if password_confirmation != password:
            print("Failed: Password Confirmation doesn't match Password")
            return ExitStatus.failure

        crypto_steganography = CryptoSteganography(password)

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
        except FileNotFoundError:
            print('Failed: Input file %s not found.' % args.input_image_file)
            return ExitStatus.failure
        except OSError as error:
            # It can be invalid file format
            print('Failed: %s' % error)
            return ExitStatus.failure

        print('Output image %s saved with success' % output_image_file)

    # Retrieve action
    elif args.command == 'retrieve':
        # Get password (the string used to derive the encryption key)
        password = getpass.getpass('Enter the key password: ').strip()
        if len(password) == 0:
            print("Failed: Password can't be empty")
            return ExitStatus.failure

        crypto_steganography = CryptoSteganography(password)

        secret = None
        try:
            secret = crypto_steganography.retrieve(args.input_image_file)
        except FileNotFoundError:
            print('Failed: Input file %s not found.' % args.input_image_file)
            return ExitStatus.failure
        except OSError as error:
            # It can be invalid file format
            print(error)
            return ExitStatus.failure

        if not secret:
            print('No valid data found')
            return ExitStatus.failure

        # Print or save to a file the data
        if args.retrieved_file:
            try:
                with open(args.retrieved_file, 'wb') as f:
                    f.write(secret)
            except TypeError:
                with open(args.retrieved_file, 'wb') as f:
                    f.write(secret.encode())

            print('%s saved with success' % args.retrieved_file)
        else:
            print(secret)

    return ExitStatus.success


def init():
    """
    Allow the script to be run standalone
    """
    if __name__ == '__main__':
        sys.exit(main())


# Run
init()
