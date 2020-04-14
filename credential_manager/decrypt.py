import os
import json 
from cryptography.fernet import Fernet
from google.cloud import kms_v1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def decrypt(ciphertext):
    key = os.environ['ENCRYPTION_KEY']
    fernet = Fernet(key)
    plaintext = fernet.decrypt(ciphertext)
    return plaintext


with open(os.path.join(BASE_DIR, 'credentials.encrypted'), 'rb') as cred:
    data = cred.read()

dec_cred = decrypt(data).decode(); 
cred = json.loads(dec_cred)
