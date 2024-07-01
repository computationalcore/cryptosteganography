import pytest
from cryptosteganography import CryptoSteganography
from Cryptodome.Cipher import AES
from PIL import Image  # Importing Image module from PIL

INPUT_IMAGE = 'tests/assets/test_image.jpg'
INPUT_MESSAGE_TEXT_FILE = 'tests/assets/test_file1.txt'
INPUT_MESSAGE_TEXT_EMPTY_FILE = 'tests/assets/test_file2.txt'
INPUT_MESSAGE_AUDIO_FILE = 'tests/assets/test_file.mp3'
OUTPUT_IMAGE = 'tests/output_files/test_image_file.png'
INVALID_IMAGE = 'tests/assets/invalid_image.jpg'

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

    with open(message_file, 'rb') as f:
        secret_message = f.read()

    crypto_steganography = CryptoSteganography(key)
    crypto_steganography.hide(
      INPUT_IMAGE,
      OUTPUT_IMAGE,
      secret_message
    )

    secret = crypto_steganography.retrieve(OUTPUT_IMAGE)

    # Ensure the retrieved message is properly decoded if it's a string
    if isinstance(secret, bytes):
        secret = secret.decode('utf-8')

    # Normalize line endings for comparison
    assert secret.replace('\r\n', '\n') == expected.replace('\r\n', '\n')


@pytest.mark.parametrize('key, message_file', [
    ('46Kj72d672628&3hd%', INPUT_MESSAGE_AUDIO_FILE)
])
def test_binary_file(key: str, message_file: str) -> None:

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


def test_decrypt_with_invalid_iv() -> None:
    key = 'test_key'
    secret_message = 'Hello World'

    crypto_steganography = CryptoSteganography(key)
    crypto_steganography.hide(
      INPUT_IMAGE,
      OUTPUT_IMAGE,
      secret_message
    )

    # Tamper with the IV to make it invalid
    with open(OUTPUT_IMAGE, 'rb') as image_file:
        data = image_file.read()

    tampered_data = data[:AES.block_size] + b'\x00' * AES.block_size + data[AES.block_size * 2:]
    with open(OUTPUT_IMAGE, 'wb') as image_file:
        image_file.write(tampered_data)

    crypto_steganography = CryptoSteganography(key)
    secret = crypto_steganography.retrieve(OUTPUT_IMAGE)

    assert secret is None


def test_retrieve_nonexistent_image() -> None:
    key = 'test_key'

    crypto_steganography = CryptoSteganography(key)
    secret = crypto_steganography.retrieve('nonexistent_image.jpg')

    assert secret is None


def test_retrieve_with_index_error() -> None:
    key = 'test_key'

    # Create an image with no hidden message
    image = Image.new('RGB', (100, 100), color = 'white')
    image.save(OUTPUT_IMAGE)

    crypto_steganography = CryptoSteganography(key)
    secret = crypto_steganography.retrieve(OUTPUT_IMAGE)

    assert secret is None
