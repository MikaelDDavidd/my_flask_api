<div align="center">

# my_flask_api

**Lightweight Flask REST API for managing user package deliveries on Firestore.**

A small Python/Flask backend that exposes CRUD endpoints for "encomendas" (package deliveries), backed by Google Firestore via the Firebase Admin SDK.

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Flask-RESTful](https://img.shields.io/badge/Flask--RESTful-API-005571)](https://flask-restful.readthedocs.io)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/docs/firestore)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-499848?logo=gunicorn&logoColor=white)](https://gunicorn.org)

</div>

---

## Overview

`my_flask_api` is the backend for a delivery/package tracking workflow. Each user (identified by `username`) has a Firestore subcollection of `encomendas` (deliveries), and the API provides endpoints to check user existence, list their deliveries, and create/read/update/delete individual records.

It is intentionally small and pragmatic: a single Flask app, one blueprint, a handful of `flask-restful` resources, and a direct connection to Firestore. The project was built as a portfolio piece to broaden a primarily Node.js / Flutter stack with Python and Google Cloud services, and to ship a deployable Heroku/Procfile-style backend end to end.

### Key Features

- **User existence check** — Quickly verify whether a user has a delivery directory in Firestore.
- **Per-user deliveries collection** — List all deliveries belonging to a given user.
- **Full CRUD on individual deliveries** — Create, read, update, and delete by document id.
- **Firestore-native** — No intermediate database; documents are stored under `encomendas/{username}/encomendas/{id}`.
- **Production-ready entrypoint** — Ships with a `Procfile` and `gunicorn` for deployment to Heroku-style platforms.

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: [Flask](https://flask.palletsprojects.com/) + [Flask-RESTful](https://flask-restful.readthedocs.io/)
- **Database**: Google Cloud [Firestore](https://firebase.google.com/docs/firestore) (via `firebase-admin`)
- **WSGI Server**: [Gunicorn](https://gunicorn.org/)
- **Deployment**: Heroku-style `Procfile`

## API Endpoints

All endpoints are mounted under the `/api` prefix.

| Method | Path                                          | Description                                  |
| ------ | --------------------------------------------- | -------------------------------------------- |
| GET    | `/api/check_user/<username>`                  | Check if a user has a Firestore directory.   |
| GET    | `/api/encomendas/<username>`                  | List all deliveries for a user.              |
| POST   | `/api/encomendas/<username>`                  | Create a new delivery for a user.            |
| GET    | `/api/encomendas/<username>/<id>`             | Fetch a single delivery by id.               |
| PUT    | `/api/encomendas/<username>/<id>`             | Replace a delivery's data.                   |
| DELETE | `/api/encomendas/<username>/<id>`             | Delete a delivery.                           |

### Example

```bash
# List all deliveries for user "mikael"
curl http://localhost:5000/api/encomendas/mikael

# Create a new delivery
curl -X POST http://localhost:5000/api/encomendas/mikael \
  -H "Content-Type: application/json" \
  -d '{"codigo": "BR1234567890", "transportadora": "Correios", "status": "em transito"}'
```

## Getting Started

### Prerequisites

- Python 3.10+
- A Firebase project with Firestore enabled
- A Firebase Admin SDK service account JSON key (download from the Firebase console)

### Installation

```bash
git clone git@gitlab.com:mikaeldavidlopes/my_flask_api.git
cd my_flask_api

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Configuration

Place your Firebase Admin SDK service account JSON at the project root and update the path in `run.py` if your filename differs:

```python
cred = credentials.Certificate('./your-service-account.json')
```

> The credentials file is sensitive — make sure it is never committed to a public repository.

### Running

```bash
# Development
python run.py

# Production (Heroku / any Procfile host)
gunicorn run:app
```

The API will be available at `http://localhost:5000/api/...`.

## Project Structure

```
my_flask_api/
├── app/
│   ├── __init__.py     # create_app factory + blueprint registration
│   ├── api.py          # Flask-RESTful resources (User, Encomenda, EncomendaDetail)
│   └── models.py       # (placeholder for future model definitions)
├── run.py              # Entrypoint: initializes Firebase Admin and runs Flask
├── requirements.txt    # Flask, flask_restful, firebase_admin, gunicorn
├── Procfile            # gunicorn run:app
└── README.md
```

## Notes & Scope

This is a small, focused backend — not a full-featured platform. It was built to:

- Practice Python + Flask in a real deployment scenario.
- Integrate directly with Firestore from a server-side runtime.
- Diversify a stack that is otherwise centered on Node.js and Flutter.

There is intentionally no auth layer, no validation library, no test suite, and no ORM — Firestore is queried directly and the surface area is kept minimal. Treat this repository as a portfolio sample of a working Flask + Firebase microservice rather than a production-grade product.

## License

Personal project — no license. All rights reserved.

---

<div align="center">
Built by <a href="https://github.com/MikaelDDavidd">Mikael David</a>
</div>
