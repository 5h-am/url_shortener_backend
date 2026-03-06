import os
import csv
import string
import time


def databaseReading () :
    try:
        if os.path.exists("urlDatabase.csv"):
            urlData = []
            with open("urlDatabase.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader :
                    urlData.append(row)
                if not urlData:
                    return None
                return urlData
    except FileNotFoundError :
        print("File not found")
        return None
    

def urlChecking (url) :
    data = databaseReading()
    if (data == None) :
        return None
    for row in data: 
        dataEncryptedUrl = row[0]
        dataUrl = row[1]
        if (dataUrl == url) :
            return dataEncryptedUrl
    return None

        

def urlShortening () :
    url = input("Enter a url : ")
    url_int = int.from_bytes(url.encode(),byteorder="big")
    temp = []
    base62 = string.digits+string.ascii_lowercase+string.ascii_uppercase

    while (url_int > 0) :
        url_int, rem = divmod(url_int,62)
        temp.append(base62[rem])
    encryptedUrl = "".join(temp)
    return encryptedUrl[0:6], url 


def databaseWriting () :
    encryptedUrl, url = urlShortening()
    urlCheck = urlChecking(url)
    link = "https://5ham.com/"
    if not urlCheck:
        print(f"\nShortened Link :- {link + encryptedUrl}")          
        with open("urlDatabase.csv", "a", newline="")as file:
            writer = csv.writer(file)
            writer.writerow([encryptedUrl,url])
    else :
        print("\nYou have already shortened this link")
        print(f"Shortened Link :- {link+urlCheck}")


def gettingUrl() :
    data = databaseReading()
    if (not data) :
        return None
    shortenedUrl = input("Enter your shortened Url : ")
    encrypedUrl = shortenedUrl.removeprefix("https://5ham.com/")
    for row in data:  
        dataEncryptedUrl = row[0]
        dataUrl = row[1]
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
        continue 
    if choice == 1:
        databaseWriting()
        time.sleep(2)      
    elif choice == 2 :
        yourUrl = gettingUrl()
        if (yourUrl) :
            print(f"\nYour Original URL :- {yourUrl}")
        else :
            print("Sorry, This doesn't match with any orignal link")
        time.sleep(2)
    elif choice == 3 :
        print("Goodbye, Have a nice day")
        break


