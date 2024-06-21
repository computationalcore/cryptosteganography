# -*- coding: utf-8 -*-

"""
A python steganography module to store messages and files AES-256 encrypted
inside an image.
"""
import argparse
import getpass
import sys

from exitstatus import ExitStatus
from importlib.metadata import version, PackageNotFoundError

import cryptosteganography.utils as utils

__author__ = 'computationalcore@gmail.com'


def get_parser(parse_this=None) -> argparse.ArgumentParser:
    """Get parser for user command line arguments."""
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
        version=get_package_version('cryptosteganography')
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

    return parser


def get_package_version(package_name):
    """Get the version of the package."""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return 'Unknown'


def _save_parse_input(args):
    """Parse input args of save action"""
    message = None
    error = None

    if args.message:
        message = args.message
    elif args.message_file:
        message, error = utils.get_data_from_file(args.message_file)

    # Validate message
    if not message and not error:
        error = "Failed: Message can't be empty"

    return message, error


def _handle_save_action(args) -> ExitStatus:
    """Save secret in file action."""
    message, error = _save_parse_input(args)

    # Get password (the string used to derive the encryption key)
    password = getpass.getpass('Enter the key password: ').strip()
    if not password:
        error = "Failed: Password can't be empty"

    if not error:
        output_image_file = utils.get_output_image_filename(args.output_image_file)

        # Hide message and save the image
        error = utils.save_output_image(
            password,
            args.input_image_file,
            message,
            output_image_file
        )

    if not error:
        print(f'Output image {output_image_file} saved with success')
        return ExitStatus.success

    print(error)
    return ExitStatus.failure


def _handle_retrieve_action(args) -> ExitStatus:
    """Retrieve secret from file action."""
    error = None

    # Get password (the string used to derive the encryption key)
    password = getpass.getpass('Enter the key password: ').strip()
    if not password:
        error = "Failed: Password can't be empty"

    if not error:
        secret, error = utils.get_secret_from_image(password, args.input_image_file)

    # Print or save to a file the data
    if not error and args.retrieved_file:
        secret = utils.save_secret_file(secret, args.retrieved_file)

    if not error:
        print(secret)
        return ExitStatus.success

    print(error)
    return ExitStatus.failure


def main() -> ExitStatus:
    """Accept arguments and run the script."""
    parser = get_parser()
    args = parser.parse_args()

    if args.command == 'save':
        return _handle_save_action(args)
    elif args.command == 'retrieve':
        return _handle_retrieve_action(args)
    else:
        parser.print_help()
        return ExitStatus.failure


def init():
    """Allow the script to be run standalone."""
    if __name__ == '__main__':
        sys.exit(main())


# Run
init()
