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
import json
import urllib.request
import urllib.parse

# ── Configuration ──────────────────────────────────────────────────────────────
USERNAME   = "tujuojal"
API_TOKEN  = "d3ff508f6022f487069a93613d59b6c415c1163c"
REPO_URL   = "https://github.com/tujuojal/jumpcomput.git"
PROJECT_DIR = f"/home/{USERNAME}/jumpcomput"
VENV_DIR    = f"/home/{USERNAME}/.virtualenvs/jumpcomput"
DOMAIN      = f"{USERNAME}.pythonanywhere.com"
PYTHON_VER  = None  # auto-detected below

API_BASE = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"

# Auto-detect the best available Python 3 version on this system
def _detect_python_ver():
    import shutil
    for ver in ("3.13", "3.12", "3.11", "3.10", "3.9"):
        if shutil.which(f"python{ver}"):
            return ver
    sys.exit("Could not find python3.x (3.9–3.13) on PATH")

PYTHON_VER = _detect_python_ver()
print(f"Detected Python version: {PYTHON_VER}")

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

class _Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text
    def json(self):
        return json.loads(self.text)

def api(method, path, data=None, json_body=None, files=None):
    """Minimal HTTP helper using only stdlib urllib."""
    url = f"{API_BASE}{path}"
    headers = {"Authorization": f"Token {API_TOKEN}"}

    body = None
    if json_body is not None:
        body = json.dumps(json_body).encode()
        headers["Content-Type"] = "application/json"
    elif files is not None:
        # Multipart form-data for file upload
        boundary = "----FormBoundary" + secrets.token_hex(8)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        parts = []
        for field_name, file_tuple in files.items():
            filename, content = file_tuple
            part = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
                f"Content-Type: text/plain\r\n\r\n"
            ).encode() + (content.encode() if isinstance(content, str) else content) + b"\r\n"
            parts.append(part)
        body = b"".join(parts) + f"--{boundary}--\r\n".encode()
    elif data is not None:
        body = urllib.parse.urlencode(data).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(url, data=body, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req) as resp:
            text = resp.read().decode()
            status = resp.status
    except urllib.error.HTTPError as e:
        text = e.read().decode()
        status = e.code

    if status not in (200, 201):
        print(f"  API {method.upper()} {path} → {status}: {text}")
    return _Response(status, text)

# ── Step 1: Clone or update the repository ──────────────────────────────────────

print("\n=== Step 1: Clone / update repository ===")
if os.path.isdir(PROJECT_DIR):
    run(f"git -C {PROJECT_DIR} pull origin master")
else:
    run(f"git clone {REPO_URL} {PROJECT_DIR}")

# ── Step 2: Create virtualenv and install dependencies ──────────────────────────

print("\n=== Step 2: Virtualenv + dependencies ===")
# PYTHON_VER is set after web app creation; venv is created/recreated in Step 3 if needed.
# We defer actual venv creation until after we know the accepted Python version.

# ── Step 3: Create web app (or confirm it exists) ──────────────────────────────

print("\n=== Step 3: Web app configuration ===")
existing = api("get", "/webapps/").json()
existing_domains = [w["domain_name"] for w in (existing if isinstance(existing, list) else [])]

if DOMAIN not in existing_domains:
    print(f"  Creating web app for {DOMAIN} ...")

    # Query the account's system image to find available Python versions
    sys_img = api("get", "/system_image/")
    print(f"  System image info: {sys_img.text}")

    # Build candidate list: dotted format AND plain integer format
    candidates = []
    for ver in ("3.13", "3.12", "3.11", "3.10", "3.9"):
        candidates.append(ver)
        candidates.append(ver.replace(".", ""))   # "313", "312", …

    created = False
    for try_ver in candidates:
        r = api("post", "/webapps/", data={"domain_name": DOMAIN, "python_version": try_ver})
        if r.status_code in (200, 201):
            PYTHON_VER = try_ver
            created = True
            print(f"  Web app created with Python version string '{PYTHON_VER}'")
            break
        body = json.loads(r.text) if r.text else {}
        if body.get("error_type") != "invalid_python_version":
            sys.exit(f"Failed to create web app: {r.text}")
    if not created:
        sys.exit(
            "Could not create web app — no supported Python version found.\n"
            "Please create the web app manually in the PythonAnywhere Web tab,\n"
            "then re-run this script (it will skip creation and configure the rest)."
        )
else:
    print(f"  Web app {DOMAIN} already exists, updating configuration ...")
    # Read the Python version the existing web app was created with
    webapp_info = api("get", f"/webapps/{DOMAIN}/").json()
    PYTHON_VER = webapp_info.get("python_version", PYTHON_VER)
    print(f"  Using existing web app Python version: {PYTHON_VER}")

# ── Create virtualenv now that we know the Python version ──────────────────────

print("\n=== Step 2b: Create virtualenv ===")
if os.path.isdir(VENV_DIR):
    # Check if it uses the right Python version
    venv_python = os.path.realpath(f"{VENV_DIR}/bin/python")
    if f"python{PYTHON_VER}" not in venv_python:
        print(f"  Removing old venv (wrong Python version)")
        run(f"rm -rf {VENV_DIR}", check=False)

if not os.path.isdir(VENV_DIR):
    # --system-site-packages reuses PythonAnywhere's pre-installed numpy/scipy/matplotlib
    run(f"python{PYTHON_VER} -m venv --system-site-packages {VENV_DIR}")

run(f"{VENV_DIR}/bin/pip install --upgrade pip -q")
# Only install packages not already available system-wide (flask, wtforms)
run(f"{VENV_DIR}/bin/pip install flask wtforms -q")

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
    r = api("post", f"/webapps/{DOMAIN}/env_variables/", json_body={"name": "SECRET_KEY", "value": secret_key})
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
