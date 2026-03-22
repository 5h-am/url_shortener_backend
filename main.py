from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS
import string
import sqlite3

app = Flask(__name__)
CORS(app)



domain_name = "http://127.0.0.1:5000/5ham/"

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS url_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT UNIQUE,
            url TEXT NOT NULL
        )
        """)

init_db()

@app.route("/")
def home():
    return jsonify({"message": "Backend working!"})

def databaseReading (short_url) :
    try:
        with sqlite3.connect("database.db")as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM url_records WHERE short_url = ?",(short_url,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
    except sqlite3.OperationalError :
        return None
    

    
def base62encoding(count):
    temp = []
    base62 = string.digits+string.ascii_lowercase+string.ascii_uppercase
    if count == 0:
        return base62[0]
    num = count
    while (num > 0) :
        num, rem = divmod(num,62)
        temp.append(base62[rem])
    encodedUrl = "".join(reversed(temp)) 
    return encodedUrl

@app.route("/NotFound")
def notFound():
    return "<h2>Url Not Found</h2>"

@app.route("/5ham/<string:shortUrl>")
def gettingUrl(shortUrl) :   
    data = databaseReading(shortUrl)
    if not data:
        return redirect(url_for("notFound")) 
    return  redirect(data)


@app.route("/shorten", methods=["POST"])
def urlShortening () :
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing URL"}), 400
    url = data.get("url")
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL"}), 400
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO url_records (url) VALUES (?)",(url,))
        id_value = cursor.lastrowid
        short_code = base62encoding(id_value)
        cursor.execute("UPDATE url_records SET short_url=? WHERE id=?",(short_code, id_value))
        conn.commit()
        return jsonify({"shortenedUrl":short_code})




