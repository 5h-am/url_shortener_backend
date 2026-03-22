# URL Shortener — Backend

A Flask REST API for shortening URLs, storing mappings in SQLite, and redirecting short URLs to their originals.

**Live API:** [https://url-shortener-backend-b41o.onrender.com](https://url-shortener-backend-b41o.onrender.com)
**Frontend Repo:** [url-shortener-frontend](https://github.com/5h-am/url_shortener) → [https://url-shortener-tawny-phi.vercel.app](https://url-shortener-tawny-phi.vercel.app)

---

## Tech Stack

- **Flask** — Web framework
- **SQLite** — Database
- **Flask-CORS** — Cross-origin support

---

## Features

- Shortens any valid `http://` or `https://` URL
- Stores mappings in a persistent SQLite database
- Redirects short URLs to their original destination
- Base62 encoding for compact short codes

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone <your-backend-repo-url>
cd url-shortener-backend
pip install -r requirements.txt
```

### Running Locally

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`.

The database (`database.db`) is created automatically on first run.

---

## API Reference

### `POST /shorten`

Shortens a URL.

**Request body:**
```json
{ "url": "https://example.com" }
```

**Response:**
```json
{ "shortenedUrl": "aB3xYz" }
```

**Errors:**
- `400` — Missing or invalid URL

---

### `GET /5ham/<shortUrl>`

Redirects to the original URL, or to `/NotFound` if the code doesn't exist.

---

### `GET /NotFound`

Returns a plain HTML not-found message.

---

## Deployment

Deployed on **Render** (free tier). Uses `gunicorn` as the WSGI server.

**Start command:**
```
gunicorn app:app
```

**Required files in repo:**
- `requirements.txt` — all dependencies
- `app.py` — main application

> **Note:** Render's free tier spins down after inactivity. The first request after a period of inactivity may take 30–60 seconds.

---

## Project Structure

```
app.py            # Main Flask application
database.db       # SQLite database (auto-created)
requirements.txt  # Python dependencies
```