echo off

call C:\DEV\python372\python --version

set FLASK_APP=mainWebApp.py

call C:\DEV\python372\python -m flask run