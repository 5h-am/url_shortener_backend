import os
import csv
import string
import time

domain_name = "https://5h-am.com/"
def databaseReading () :
    try:
        urlData = []
        with open("urlDatabase.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader :
                urlData.append(row)
            if not urlData:
                return []
            return urlData
    except FileNotFoundError :
        print("File not found")
        return None
    

def counter_writing (count) :
    with open("counter.txt","w")as f:
        f.write(str(count))

def counter_reading () :
    if os.path.exists("counter.txt"):
        with open("counter.txt", "r")as f:
            count = f.read()
            return count
    else :
        return 0  

def urlShortening () :
    url = input("Enter a url : ")
    previous_count = counter_reading()
    now_count = int(previous_count)
    counter_writing(now_count+1)
    temp = []
    base62 = string.ascii_lowercase+string.ascii_uppercase+string.digits
    if now_count == 0:
        temp.append(base62[0])
    while (now_count > 0) :
        now_count, rem = divmod(now_count,62)
        temp.append(base62[rem])
    encryptedUrl = "".join(reversed(temp)) 
    return encryptedUrl, url 


def databaseWriting () :
    encryptedUrl, url = urlShortening()
    print(f"\nShortened Link :- {domain_name+ encryptedUrl}")          
    with open("urlDatabase.csv", "a", newline="")as file:
        writer = csv.writer(file)
        writer.writerow([encryptedUrl,url])



def gettingUrl() :
    data = databaseReading()
    if (not data) :
        return None
    shortenedUrl = input("Enter your shortened Url : ")
    encrypedUrl = shortenedUrl.removeprefix(domain_name)
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


