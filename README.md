# LinkVault

LinkVault is a small web app I built to save and manage bookmarks. Instead of keeping links all over the place, this lets you store them in one spot and access them after logging in.

## Live display demo

[Open the LinkVault display demo](https://fsrkh12-arch.github.io/LinkVault/)

The GitHub Pages version is a browser-only display demo. The Flask app in this repository is the secure version with accounts and SQLite data. The Pages demo deploys automatically whenever this repository is updated.

The goal of this project was to practice Flask, databases, and basic full-stack concepts without using heavy frameworks.

What it does

- Lets users sign up and log in
- Passwords are hashed (not stored as plain text)
- Users can add links with a title and URL
- Saved links are shown on a simple dashboard
- Links can be deleted
- Data is saved using SQLite

Tools used

- Python
- Flask
- HTML and CSS
- SQLite
- Werkzeug for password hashing

Everything is kept simple on purpose. No React, no external services.

Folder structure

linkvault/
- app.py
- database.db (created automatically)
- templates/
  - login.html
  - register.html
  - dashboard.html
- static/
  - style.css
- .gitignore
- README.txt

How to run it

1. Install the dependencies:
   pip install flask werkzeug

2. Run the app:
   python app.py

3. Open your browser and go to:
   http://127.0.0.1:5000

The database file will be created automatically the first time you run the app. For a real deployment, set a long random `SECRET_KEY` environment variable before running Flask.

## Deploy on Koyeb

This repository includes a `Procfile` for Koyeb. Create a GitHub-based Web Service, choose the buildpack option, and add these environment variables in Koyeb:

- `SECRET_KEY`: a long, random value kept private
- `COOKIE_SECURE`: `true`

Koyeb provides the `PORT` automatically. The free tier is suitable for displaying this project, but the local SQLite database is not a permanent production database, so do not use it for important data.

## Render display deployment

`render.yaml` can create the Flask web service using the free plan. Render generates the session secret automatically. This is for displaying the app: its free web service can restart and local SQLite data is not permanent.

Why I built this

This project helped me understand how Flask routes work, how user authentication is handled, how to store and retrieve data with SQLite, and how the frontend and backend connect.

It’s not meant to be fancy. It’s meant to be clear and easy to understand.

Possible improvements

- Tags, search, and filtering are included.
- Deploy it online
