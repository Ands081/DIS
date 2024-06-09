# DIS

Run the code below to install the dependencies.
    pip install -r requirements.txt

For windows do before database loading
    cmd /c chcp 65001

Set dbname, user and password in __init__.py

Initialize loaddb.sql
    psql -d kebab -U postgres -W -f src/loaddb.sql

Run Web-App
    python run.py