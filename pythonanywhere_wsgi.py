# PythonAnywhere WSGI configuration file for jumpcomput
#
# Instructions:
# 1. In the PythonAnywhere web dashboard, go to the Web tab
# 2. Create a new web app (or edit existing) and choose "Manual configuration"
# 3. Set the path to this file as the WSGI configuration file, OR
#    copy the contents of this file into the WSGI file at:
#    /var/www/tujuojal_pythonanywhere_com_wsgi.py
#
# 4. In the "Virtualenv" section, set the path to your virtualenv, e.g.:
#    /home/tujuojal/.virtualenvs/jumpcomput
#
# 5. In a PythonAnywhere Bash console, install dependencies:
#    cd ~/jumpcomput && pip install -r requirements.txt
#
# 6. Set the SECRET_KEY environment variable in the Web tab > Environment variables:
#    SECRET_KEY = <generate a strong random string>

import sys
import os

# Path to the project directory on PythonAnywhere
path = '/home/tujuojal/jumpcomput'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application  # noqa
