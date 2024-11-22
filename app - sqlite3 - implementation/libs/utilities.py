import hashlib
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

class Utilities:
    @staticmethod
    def hash_data(data):
        """
        Hash data using SHA-256 algorithm.
        Args:
            data (str): Data to be hashed.

        Returns:
            str: Hash value of the data.
        """
        hasher = hashlib.sha256()
        hasher.update(data.encode())
        return hasher.hexdigest()

    @staticmethod
    def generate_keys():
        """
        Generate public and private key pair using Elliptic Curve Cryptography (ECC).
        Returns:
            tuple: Public and private key pair.
        """
        private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def sign_data(private_key, data):
        """
        Sign data using a private key.
        Args:
            private_key (object): EC private key.
            data (dict): Data to be signed.

        Returns:
            bytes: Signature of the data.
        """
        serialized_data = json.dumps(data, sort_keys=True).encode()
        signature = private_key.sign(serialized_data, ec.ECDSA(hashes.SHA256()))
        return signature

    @staticmethod
    def verify_signature(public_key, data, signature):
        """
        Verify the signature of data using a public key.
        Args:
            public_key (object): EC public key.
            data (dict): Data to be verified.
            signature (bytes): Signature of the data.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        serialized_data = json.dumps(data, sort_keys=True).encode()
        try:
            public_key.verify(signature, serialized_data, ec.ECDSA(hashes.SHA256()))
            return True
        except:
            return False
