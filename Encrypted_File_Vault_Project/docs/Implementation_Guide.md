# Implementation and Demonstration Guide

## Setup on Windows PowerShell
1. Open this folder in VS Code.
2. Create a virtual environment:
   `py -m venv .venv`
3. Activate it:
   `.\.venv\Scripts\Activate.ps1`
4. If PowerShell blocks activation, run this for the current terminal:
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
   Then activate again.
5. Install packages:
   `python -m pip install -r requirements.txt`
6. Copy `.env.example` to `.env`.
7. Generate a Fernet key:
   `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
8. Paste the generated key into `FERNET_KEY` in `.env`. Also replace `SECRET_KEY` with a different random secret.
9. Start the app:
   `python run.py`
10. Open `http://127.0.0.1:5000`.

## Demo flow
1. Register and log in.
2. Upload a harmless sample text file.
3. Show the encrypted `.enc` blob in `storage/encrypted`.
4. Download the file and compare its contents to the original.
5. Create a share link with a short expiry and open it in a private browser window.
6. Demonstrate that a second user cannot see the first user's private vault.
7. Delete the file and show that the share link no longer works.

## Screenshots to include
Landing page, registration, login, empty vault, uploaded file list, encrypted blob, downloaded file, share URL with expiry, and database tables.

## Security notes
Keep `.env` and the encryption key private. Back up the key securely; changing or losing it makes existing encrypted files unreadable. Enable HTTPS and secure cookies for deployment. Add CSRF protection, rate limiting, audit logging, malware scanning, quotas, and security review before public use.
