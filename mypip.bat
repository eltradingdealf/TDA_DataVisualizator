echo off


call C:\DEV\python372\python --version

call C:\DEV\python372\Scripts\pip --version
call C:\DEV\python372\python -m pip install --upgrade pip
call C:\DEV\python372\Scripts\pip --version

call C:\DEV\python372\Scripts\pip install --upgrade setuptools
call C:\DEV\python372\Scripts\pip install --upgrade requests
call C:\DEV\python372\Scripts\pip install --upgrade simpleJson
call C:\DEV\python372\Scripts\pip install --upgrade pytz
call C:\DEV\python372\Scripts\pip install --upgrade pyparsing
call C:\DEV\python372\Scripts\pip install --upgrade cmd2
call C:\DEV\python372\Scripts\pip install --upgrade PyMySQL
call C:\DEV\python372\Scripts\pip install --upgrade pymongo
call C:\DEV\python372\Scripts\pip install --upgrade colorama
call C:\DEV\python372\Scripts\pip install --upgrade astroid
call C:\DEV\python372\Scripts\pip install --upgrade pylint
call C:\DEV\python372\Scripts\pip install --upgrade isort
call C:\DEV\python372\Scripts\pip install --upgrade pyperclip
call C:\DEV\python372\Scripts\pip install --upgrade numpy matplotlib
call C:\DEV\python372\Scripts\pip install --upgrade click
call C:\DEV\python372\Scripts\pip install --upgrade flask
call C:\DEV\python372\Scripts\pip install --upgrade Flask-RESTful
call C:\DEV\python372\Scripts\pip install --upgrade Flask-Cors
call C:\DEV\python372\Scripts\pip install --upgrade urllib3

call C:\DEV\python372\Scripts\pip list