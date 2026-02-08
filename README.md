LinkVault

LinkVault is a small web app I built to save and manage bookmarks. Instead of keeping links all over the place, this lets you store them in one spot and access them after logging in.

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

The database file will be created automatically the first time you run the app.

Why I built this

This project helped me understand how Flask routes work, how user authentication is handled, how to store and retrieve data with SQLite, and how the frontend and backend connect.

It’s not meant to be fancy. It’s meant to be clear and easy to understand.

Possible improvements

- Add categories or tags
- Add search and filtering
- Add priority levels
- Deploy it online
