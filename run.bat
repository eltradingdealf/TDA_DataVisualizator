echo off

call C:\DEV\python3\python --version

set FLASK_APP=mainWebApp.py

call C:\DEV\python3\python -m flask run