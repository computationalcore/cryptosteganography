import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from stegano import lsb
from PIL import UnidentifiedImageError, Image
import os

__author__ = 'computationalcore@gmail.com'


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

        # Encrypt the random initialization vector concatenated
        # with the padded data
        cypher_data = encryption_suite.encrypt(iv + pad(data, self.block_size))

        # Convert the cypher byte string to a base64 string to avoid
        # decode padding error
        cypher_data = base64.b64encode(cypher_data).decode()

        # Hide the encrypted message in the image with the LSB
        # (Least Significant Bit) technique.
        secret = lsb.hide(input_filename, cypher_data)
        # Save the image file
        secret.save(output_filename)

    def retrieve(self, input_image_file):
        """
        Retrieve the encrypted data from the image.
        :param input_image_file: Input image file path
        :return:
        """
        try:
            cypher_data = lsb.reveal(input_image_file)
        except (UnidentifiedImageError, FileNotFoundError, IndexError):
            return None

        if not cypher_data:
            return None

        cypher_data = base64.b64decode(cypher_data)
        # Retrieve the dynamic initialization vector saved
        iv = cypher_data[:AES.block_size]
        # Retrieved the cypher data
        cypher_data = cypher_data[AES.block_size:]

        try:
            decryption_suite = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = unpad(
                decryption_suite.decrypt(cypher_data),
                self.block_size
            )
            try:
                return decrypted_data.decode('utf-8')
            except UnicodeDecodeError:
                # Binary data - returns as it is
                return decrypted_data
        except ValueError:
            return None
