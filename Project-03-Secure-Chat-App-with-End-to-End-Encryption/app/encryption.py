from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.backends import default_backend
import os
import base64

# -------- RSA Key Functions --------

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_public_key(public_key):
    return base64.b64encode(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    ).decode('utf-8')

def deserialize_public_key(public_key_str):
    return serialization.load_pem_public_key(
        base64.b64decode(public_key_str.encode('utf-8')), backend=default_backend()
    )

def serialize_private_key(private_key):
    return base64.b64encode(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    ).decode('utf-8')

def deserialize_private_key(private_key_str):
    return serialization.load_pem_private_key(
        base64.b64decode(private_key_str.encode('utf-8')), password=None, backend=default_backend()
    )

# -------- AES Functions --------

def generate_aes_key(length=32):
    return os.urandom(length)  # 256-bit key

def encrypt_aes(key, plaintext):
    iv = os.urandom(16)
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_aes(key, ciphertext_b64):
    data = base64.b64decode(ciphertext_b64.encode('utf-8'))
    iv, ciphertext = data[:16], data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

# -------- RSA Encrypt/Decrypt AES Key --------

def encrypt_aes_key_rsa(aes_key, public_key):
    return base64.b64encode(
        public_key.encrypt(
            aes_key,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
    ).decode('utf-8')

def decrypt_aes_key_rsa(enc_key_b64, private_key):
    enc_key = base64.b64decode(enc_key_b64.encode('utf-8'))
    return private_key.decrypt(
        enc_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )