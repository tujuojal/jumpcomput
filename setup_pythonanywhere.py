#!/usr/bin/env python3
"""
PythonAnywhere automated deployment script for jumpcomput.

Run this script ONCE from a PythonAnywhere Bash console:

    python3 setup_pythonanywhere.py

It will:
  1. Clone/update the GitHub repo
  2. Create a virtualenv and install dependencies
  3. Create/configure the web app via PythonAnywhere API
  4. Upload the WSGI configuration
  5. Reload the web app

The app will then be live at https://tujuojal.pythonanywhere.com
"""

import os
import sys
import subprocess
import secrets
import requests

# ── Configuration ──────────────────────────────────────────────────────────────
USERNAME   = "tujuojal"
API_TOKEN  = "d3ff508f6022f487069a93613d59b6c415c1163c"
REPO_URL   = "https://github.com/tujuojal/jumpcomput.git"
PROJECT_DIR = f"/home/{USERNAME}/jumpcomput"
VENV_DIR    = f"/home/{USERNAME}/.virtualenvs/jumpcomput"
DOMAIN      = f"{USERNAME}.pythonanywhere.com"
PYTHON_VER  = "3.10"

API_BASE = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"
HEADERS  = {"Authorization": f"Token {API_TOKEN}"}

# ── Helpers ─────────────────────────────────────────────────────────────────────

def run(cmd, check=True):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if check and result.returncode != 0:
        sys.exit(f"Command failed with exit code {result.returncode}")
    return result

def api(method, path, **kwargs):
    url = f"{API_BASE}{path}"
    resp = getattr(requests, method)(url, headers=HEADERS, **kwargs)
    if resp.status_code not in (200, 201):
        print(f"  API {method.upper()} {path} → {resp.status_code}: {resp.text}")
    return resp

# ── Step 1: Clone or update the repository ──────────────────────────────────────

print("\n=== Step 1: Clone / update repository ===")
if os.path.isdir(PROJECT_DIR):
    run(f"git -C {PROJECT_DIR} pull origin master")
else:
    run(f"git clone {REPO_URL} {PROJECT_DIR}")

# ── Step 2: Create virtualenv and install dependencies ──────────────────────────

print("\n=== Step 2: Virtualenv + dependencies ===")
if not os.path.isdir(VENV_DIR):
    run(f"python{PYTHON_VER} -m venv {VENV_DIR}")
run(f"{VENV_DIR}/bin/pip install --upgrade pip -q")
run(f"{VENV_DIR}/bin/pip install -r {PROJECT_DIR}/requirements.txt -q")

# ── Step 3: Create web app (or confirm it exists) ──────────────────────────────

print("\n=== Step 3: Web app configuration ===")
existing = api("get", "/webapps/").json()
existing_domains = [w["domain_name"] for w in (existing if isinstance(existing, list) else [])]

if DOMAIN not in existing_domains:
    print(f"  Creating web app for {DOMAIN} ...")
    r = api("post", "/webapps/", data={
        "domain_name": DOMAIN,
        "python_version": PYTHON_VER,
    })
    if r.status_code not in (200, 201):
        sys.exit(f"Failed to create web app: {r.text}")
    print(f"  Web app created: {DOMAIN}")
else:
    print(f"  Web app {DOMAIN} already exists, updating configuration ...")

# ── Step 4: Set virtualenv path ────────────────────────────────────────────────

print("\n=== Step 4: Set virtualenv path ===")
r = api("patch", f"/webapps/{DOMAIN}/", data={"virtualenv_path": VENV_DIR})
print(f"  Virtualenv set to: {VENV_DIR} (status {r.status_code})")

# ── Step 5: Upload WSGI file ───────────────────────────────────────────────────

print("\n=== Step 5: Upload WSGI configuration ===")

# PythonAnywhere places the WSGI file at a fixed path
wsgi_path = f"/var/www/{USERNAME}_pythonanywhere_com_wsgi.py"

wsgi_content = f"""# Auto-generated WSGI config for jumpcomput on PythonAnywhere
import sys
import os

path = '{PROJECT_DIR}'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application  # noqa
"""

r = api("post", f"/files/path{wsgi_path}", files={"content": ("wsgi.py", wsgi_content)})
print(f"  WSGI file uploaded to {wsgi_path} (status {r.status_code})")

# Point the web app at the WSGI file
r = api("patch", f"/webapps/{DOMAIN}/", data={"wsgi_file_path": wsgi_path})
print(f"  WSGI path set on web app (status {r.status_code})")

# ── Step 6: Set SECRET_KEY environment variable ────────────────────────────────

print("\n=== Step 6: Environment variables ===")

# Check if SECRET_KEY already set
env_resp = api("get", f"/webapps/{DOMAIN}/env_variables/")
existing_env = {e["name"]: e for e in (env_resp.json() if env_resp.status_code == 200 else [])} if isinstance(env_resp.json(), list) else {}

if "SECRET_KEY" not in existing_env:
    secret_key = secrets.token_hex(32)
    r = api("post", f"/webapps/{DOMAIN}/env_variables/", json={"name": "SECRET_KEY", "value": secret_key})
    print(f"  SECRET_KEY generated and set (status {r.status_code})")
else:
    print("  SECRET_KEY already set, skipping.")

# ── Step 7: Reload the web app ────────────────────────────────────────────────

print("\n=== Step 7: Reload web app ===")
r = api("post", f"/webapps/{DOMAIN}/reload/")
print(f"  Reload status: {r.status_code} {r.text}")

# ── Done ──────────────────────────────────────────────────────────────────────

print(f"""
=== Deployment complete! ===

Your app is live at: https://{DOMAIN}

To update after a future git push, run in a PythonAnywhere Bash console:
    git -C {PROJECT_DIR} pull origin master
    {VENV_DIR}/bin/pip install -r {PROJECT_DIR}/requirements.txt
    # then reload the web app from the Web tab, or:
    python3 {PROJECT_DIR}/setup_pythonanywhere.py
""")
