from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os
import csv


def databaseReading () :
    try:
        if os.path.exists("urlDatabase.csv"):
            urlData = []
            with open("urlDatabase.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader :
                    urlData.append(row)
                return urlData
    except FileNotFoundError :
        print("File not found")
        return None
    

def urlChecking (url) :
    data = databaseReading()
    if (data == None) :
        return None
    for i in range(0,len(data),1):
        dataUrl = data[i]["url"]
        dataEncryptedUrl = data[i]["encryptedUrl"]
        if (dataUrl == url) :
            return dataEncryptedUrl
    return None

        

def urlShortening () :
    url = input("Enter a url : ").encode()
    salt = os.urandom(4)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=8,
        salt=salt,
        iterations=10000,
        backend=default_backend()
    )
    encryptedUrl = base64.urlsafe_b64encode(kdf.derive(url)).rstrip(b"=")
    return encryptedUrl, url 


def databaseWriting () :
    encryptedUrl, url = urlShortening()
    urlCheck = urlChecking(url.decode())
    link = "https://5ham/"
    if not urlCheck:
        print(f"\nShortened Link :- {link + encryptedUrl.decode()}")          
        if (os.path.exists("urlDatabase.csv")) :
            with open("urlDatabase.csv", "a", newline="")as file:
                writer = csv.DictWriter(file, fieldnames=["encryptedUrl", "url"])
                writer.writerow({"encryptedUrl":encryptedUrl.decode(),"url":url.decode()})
        else :
            with open("urlDatabase.csv", "w", newline="")as file:
                writer = csv.DictWriter(file, fieldnames=["encryptedUrl", "url"])
                writer.writeheader()
                writer.writerow({"encryptedUrl":encryptedUrl.decode(),"url":url.decode()})
    else :
        print(f"\nShortened Link :- {link+urlCheck}")


def gettingUrl() :
    data = databaseReading()
    if (not data) :
        return None
    shortenedUrl = input("Enter your shortened Url : ")
    encrypedUrl = shortenedUrl.removeprefix("https://5ham/")
    for i in range(0,len(data),1):
        dataUrl = data[i]["url"]
        dataEncryptedUrl = data[i]["encryptedUrl"]
        if (dataEncryptedUrl == encrypedUrl) :
            return dataUrl
    return None

    
while True:
    print()
    print("-"*100)
    print("URL Shortener")
    print("-"*100)
    print("\n1.Shorten your URL")
    print('2.Get Your Original URL')
    print("3.Exit the Program\n")
    
    try :
        choice = int(input("\nEnter your choice (1/2/3) : "))
        if choice not in range(1,4) :
            raise ValueError
    except ValueError as e :
        print("\nInvalid Input ",e)
    if choice == 1:
        databaseWriting()
    elif choice == 2 :
        yourUrl = gettingUrl()
        if (yourUrl) :
            print(f"\nYour Original URL :- {yourUrl}")
    elif choice == 3 :
        break



