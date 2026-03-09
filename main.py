import os
import csv
import string
import time
import sqlite3

domain_name = "https://5h-am.com/"
def databaseReading (short_url) :
    try:
        with sqlite3.connect("database.db")as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM url_records WHERE short_url == ?",(short_url,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
    except FileNotFoundError :
        print("File not found")
        return None
    



def counter_reading () :
    if os.path.exists("database.db"):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id) FROM url_records")
            count = cursor.fetchone()[0]
            return count
    else :
        return 0  

def urlShortening () :
    url = input("Enter a url : ")
    if not url.startswith("https://") :
        print("Error, Only URLs are allowed")
        return None, None
    count = counter_reading()
    count += 1
    temp = []
    base62 = string.digits+string.ascii_lowercase+string.ascii_uppercase
    num = count
    while (num > 0) :
        num, rem = divmod(num,62)
        temp.append(base62[rem])
    encryptedUrl = "".join(reversed(temp)) 
    return encryptedUrl, url 


def databaseWriting () :
    encryptedUrl, url = urlShortening()
    if encryptedUrl:
        print(f"\nShortened Link :- {domain_name+ encryptedUrl}")          
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            conn.execute("INSERT INTO url_records (short_url, url) VALUES(?,?)",(encryptedUrl,url))
            conn.commit()

def gettingUrl() :   
    shortenedUrl = input("Enter your shortened Url : ")
    encryptedUrl = shortenedUrl.removeprefix(domain_name)
    data = databaseReading(encryptedUrl)
    return data
 
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
        time.sleep(1)      
    elif choice == 2 :
        yourUrl = gettingUrl()
        if (yourUrl) :
            print(f"\nYour Original URL :- {yourUrl}")
        else :
            print("\nSorry, This doesn't match with any orignal link")
        time.sleep(1)
    elif choice == 3 :
        print("\nGoodbye, Have a nice day")
        break


