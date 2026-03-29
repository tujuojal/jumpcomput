#!/bin/bash
# Run this script in a PythonAnywhere Bash console to set up / update the deployment.
#
# First-time setup:
#   bash deploy_pythonanywhere.sh setup
#
# Updating after a git push:
#   bash deploy_pythonanywhere.sh update

REPO_URL="https://github.com/tujuojal/jumpcomput.git"
PROJECT_DIR="$HOME/jumpcomput"
VENV_DIR="$HOME/.virtualenvs/jumpcomput"

setup() {
    echo "=== Setting up jumpcomput on PythonAnywhere ==="

    # Clone the repository
    if [ -d "$PROJECT_DIR" ]; then
        echo "Directory $PROJECT_DIR already exists, pulling latest changes..."
        cd "$PROJECT_DIR" && git pull origin master
    else
        git clone "$REPO_URL" "$PROJECT_DIR"
    fi

    # Create virtualenv if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtualenv..."
        python3 -m venv "$VENV_DIR"
    fi

    # Install/update dependencies
    echo "Installing dependencies..."
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

    echo ""
    echo "=== Setup complete! ==="
    echo ""
    echo "Next steps in the PythonAnywhere Web tab:"
    echo "1. Set WSGI configuration file to: $PROJECT_DIR/pythonanywhere_wsgi.py"
    echo "   OR copy its contents to /var/www/tujuojal_pythonanywhere_com_wsgi.py"
    echo "2. Set Virtualenv path to: $VENV_DIR"
    echo "3. Add environment variable: SECRET_KEY=<your-secret-key>"
    echo "4. Click 'Reload' to apply changes"
}

update() {
    echo "=== Updating jumpcomput deployment ==="

    cd "$PROJECT_DIR" && git pull origin master

    echo "Updating dependencies..."
    "$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

    echo ""
    echo "=== Update complete! ==="
    echo "Go to the PythonAnywhere Web tab and click 'Reload' to apply changes."
}

case "$1" in
    setup)  setup ;;
    update) update ;;
    *)
        echo "Usage: $0 {setup|update}"
        echo "  setup  - First-time setup: clone repo, create venv, install deps"
        echo "  update - Pull latest code and update dependencies"
        exit 1
        ;;
esac
