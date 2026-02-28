from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import json
import os
import csv



url = input("Enter a url : ").encode()
def urlShortening () :
    salt = os.urandom(4)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=8,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
    encryptedUrl = base64.urlsafe_b64encode(kdf.derive(url)).rstrip(b"=")
    return encryptedUrl



def databaseWriting () :
    encryptedUrl = urlShortening()
    if (os.path.exists("urlDatabase.csv")) :
        with open("urlDatabase.csv", "a", newline="")as file:
            writer = csv.DictWriter(file, fieldnames=["encryptedUrl", "url"])
            writer.writerow({"encryptedUrl":encryptedUrl.decode(),"url":url.decode()})
    else :
        with open("urlDatabase.csv", "w", newline="")as file:
            writer = csv.DictWriter(file, fieldnames=["encryptedUrl", "url"])
            writer.writeheader()
            writer.writerow({"encryptedUrl":encryptedUrl.decode(),"url":url.decode()})


