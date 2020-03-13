import pytest

from cryptosteganography import CryptoSteganography

INPUT_IMAGE = 'tests/assets/test_image.jpg'
INPUT_MESSAGE_TEXT_FILE = 'tests/assets/test_file1.txt'
INPUT_MESSAGE_TEXT_EMPTY_FILE = 'tests/assets/test_file2.txt'
INPUT_MESSAGE_AUDIO_FILE = 'tests/assets/test_file.mp3'
OUTPUT_IMAGE = 'tests/output_files/test_image_file.png'


@pytest.mark.parametrize('key, secret_message, expected', [
    ('123456@100%', 'Hello World', 'Hello World'),
    ('8fjf&F0g3d_92019s', 'Vin Busquet', 'Vin Busquet'),
    (
      '8fjf&_39dhG5_3Sz@900@12a',
      'CryptoSteganography is very cool!!!',
      'CryptoSteganography is very cool!!!'
    ),
    ('你好，世界', 'My frienD', 'My frienD'),
    ('你好，世界', '你好，世界', '你好，世界'),
])
def test_message(key: str, secret_message: str, expected: str) -> None:

    crypto_steganography = CryptoSteganography(key)
    crypto_steganography.hide(
      INPUT_IMAGE,
      OUTPUT_IMAGE,
      secret_message
    )

    secret = crypto_steganography.retrieve(OUTPUT_IMAGE)

    assert secret == expected


@pytest.mark.parametrize('key, message_file, expected', [
    (
        'fn48&3hdh3',
        INPUT_MESSAGE_TEXT_FILE,
        """Hello World File
Hi

Olá


你好，世界"""
    ),
    ('46Kj72d672628&3hd%', INPUT_MESSAGE_TEXT_EMPTY_FILE, '')
])
def test_text_file(key: str, message_file: str, expected: str) -> None:

    secret_message = None
    with open(message_file, 'rb') as f:
        secret_message = f.read()

    crypto_steganography = CryptoSteganography(key)
    crypto_steganography.hide(
      INPUT_IMAGE,
      OUTPUT_IMAGE,
      secret_message
    )

    secret = crypto_steganography.retrieve(OUTPUT_IMAGE)

    assert secret == expected


@pytest.mark.parametrize('key, message_file', [
    ('46Kj72d672628&3hd%', INPUT_MESSAGE_AUDIO_FILE)
])
def test_binary_file(key: str, message_file: str) -> None:

    secret_message = None
    with open(message_file, 'rb') as f:
        secret_message = f.read()

    crypto_steganography = CryptoSteganography(key)
    crypto_steganography.hide(
      INPUT_IMAGE,
      OUTPUT_IMAGE,
      secret_message
    )

    secret = crypto_steganography.retrieve(OUTPUT_IMAGE)

    assert secret == secret_message


@pytest.mark.parametrize('key', [
    ('46Kj72d672628&3hd%')
])
def test_retrieve_from_raw_image(key: str) -> None:

    crypto_steganography = CryptoSteganography(key)
    secret = crypto_steganography.retrieve(INPUT_IMAGE)

    assert secret is None


@pytest.mark.parametrize('key', [
    ('46Kj72d672628&3hd%')
])
def test_save_invalid(key: str) -> None:

    crypto_steganography = CryptoSteganography(key)
    secret = crypto_steganography.retrieve(INPUT_IMAGE)

    assert secret is None


@pytest.mark.parametrize('key', [
    ('46Kj72d672628&3hd%')
])
def test_invalid_key(key: str) -> None:

    crypto_steganography = CryptoSteganography(key)
    crypto_steganography.hide(
      INPUT_IMAGE,
      OUTPUT_IMAGE,
      'test invalid'
    )

    crypto_steganography = CryptoSteganography('jfffhh')
    secret = crypto_steganography.retrieve(OUTPUT_IMAGE)

    assert secret is None
