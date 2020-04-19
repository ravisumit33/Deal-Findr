import os
from cryptography.fernet import Fernet
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def encrypt(plaintext):
    key = os.environ['ENCRYPTION_KEY']
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(plaintext)
    return ciphertext

def main():
    with open(os.path.join(BASE_DIR, os.environ["CRED_PATH"]), 'rb') as fp:
        data = fp.read()
    with open(os.path.join(BASE_DIR, 'credentials.encrypted'), 'wb') as fp:
        fp.write(encrypt(data))
    print("Encryption done.")
    print("Exiting...")


if __name__ == "__main__":
    main()
