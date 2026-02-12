# Video CMS - Beginner's Guide

Welcome to your new Video CMS! This guide assumes zero prior knowledge and will walk you through setting up and running the project.

## 1. Prerequisites (Already done in this environment)
- **Python 3.12+**: Make sure Python is installed.
- **Project Structure**: Created `apps/videos`, `apps/importer`, etc.

## 2. Installation (Dependencies)
If you haven't already, install the required libraries:
```bash
pip install -r requirements.txt
```

## 3. Database Setup (Already done)
We use a database to store videos. Run these commands to set it up:
```bash
python manage.py migrate
```

## 4. Create an Admin User (To view data)
You need an admin account to log in to the dashboard. Run this and follow the prompts (username, email, password):
```bash
python manage.py createsuperuser
```
*(You can use 'admin' / 'admin@example.com' / 'password123' for simplicity in development)*

## 5. Import Videos (The Core Feature)
This command fetches videos from the external API (Caobizy) and saves them to your database.
- `--pages 1`: Imports only the first page (usually ~20 videos). Increase this number for more.
```bash
python manage.py import_videos --pages 1
```

## 6. Run the Server
Start the website so you can see it in your browser:
```bash
python manage.py runserver
```

## 7. View Results
1.  Open your browser and go to: `http://127.0.0.1:8000/admin/`
2.  Log in with the superuser account you created in Step 4.
3.  Click on **Videos** or **Episodes** to see the imported data!

## Troubleshooting
- **If import fails:** Check your internet connection. The API might be down or slow.
- **If server stops:** Press `Ctrl+C` in the terminal to stop the server, then run it again.
