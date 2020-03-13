from typing import Optional, Tuple

from cryptosteganography import CryptoSteganography

__author__ = 'computationalcore@gmail.com'


def get_data_from_file(file_path: str) -> Tuple[Optional[bytes], Optional[str]]:
    data = None
    error = None
    try:
        # Try to read as binary if failed as utf-8 encoded string based file
        with open(file_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        error = 'Failed: File {} not found.'.format(file_path)

    if not data and not error:
        error = "Failed: Message file content can't be empty"

    return (data, error)


def get_secret_from_image(
    password: Optional[str],
    file_path: str
) -> Tuple[Optional[bytes], Optional[str]]:
    secret = None
    error = None

    crypto_steganography = CryptoSteganography(password)

    try:
        secret = crypto_steganography.retrieve(file_path)
    except FileNotFoundError:
        error = 'Failed: Input file {} not found.'.format(file_path)
    except OSError as os_error:
        # It can be invalid file format
        error = str(os_error)

    if not secret and not error:
        error = 'No valid data found'

    return (secret, error)


def get_output_image_filename(output_image_file: str) -> str:
    if not output_image_file:
        output_image_file = 'output.png'
    else:
        # If output image doesn't have png suffix or is in other format, force png append
        if output_image_file[-4:].lower() != '.png':
            output_image_file += '.png'

    return output_image_file


def save_output_image(
    password: Optional[str],
    input_image_file: str,
    message: Optional[bytes],
    output_image_file: str
) -> Optional[str]:

    crypto_steganography = CryptoSteganography(password)

    error = None
    try:
        crypto_steganography.hide(input_image_file, output_image_file, message)
    except FileNotFoundError:
        error = 'Failed: Input file {} not found.'.format(input_image_file)
    except OSError as os_error:
        # It can be invalid file format
        error = 'Failed: %s' % os_error

    return error


def save_secret_file(secret, retrieved_file):
    try:
        with open(retrieved_file, 'wb') as f:
            f.write(secret)
    except TypeError:
        with open(retrieved_file, 'wb') as f:
            f.write(secret.encode())

    return '{} saved with success'.format(retrieved_file)
