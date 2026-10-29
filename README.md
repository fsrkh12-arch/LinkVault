# LinkVault

LinkVault is a small bookmark manager built to explore Flask, authentication, and database-backed web applications. It keeps a user's links together and makes them easier to find later.

## Try it

- [Open the Flask app](https://linkvault-8u34.onrender.com/) — create an account to try the full application. The free service may take a while to wake up, and its SQLite data is not permanent.
- [Open the browser demo](https://fsrkh12-arch.github.io/LinkVault/) — a separate display version that keeps links in the current browser and does not use Flask accounts.

## Features

- Register and sign in; passwords are stored as hashes.
- Save links with titles and optional tags, search and filter them, mark favorites, and delete them.
- Keep each account's links separate. Forms use CSRF tokens and saved URLs are restricted to HTTP and HTTPS.

## Run locally

Requires Python. From the repository directory:

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app app run
```

Open the address printed by Flask. The app creates `database.db` automatically. For a deployment, provide a private, random `SECRET_KEY` and set `COOKIE_SECURE=true` when using HTTPS. SQLite on the included free hosting configuration is intended for demonstration, not durable storage of important data.

## Built with

Python, Flask, SQLite, Jinja templates, HTML, CSS, and Werkzeug. `render.yaml` and `Procfile` provide deployment configuration.
