import os
from google.cloud import kms_v1
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def encrypt_symmetric(plaintext):
    client = kms_v1.KeyManagementServiceClient()
    resource_name = client.crypto_key_path_path("deal-findr-33", "global", "deal_findr", "deal_findr")
    response = client.encrypt(resource_name, plaintext)
    return response.ciphertext

credentials = [
    "SECRET_KEY",
    "SQL_CONNECTION_NAME",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWD",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWD"
]

with open(os.path.join(BASE_DIR, os.environ["CRED_PATH"]), 'rb') as fp:
    data = fp.read()

with open(os.path.join(BASE_DIR, 'credentials.json.encrypted'), 'wb') as fp:
    fp.write(encrypt_symmetric(data))




