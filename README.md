# DIS

Run the code below to install the dependencies.
    pip install -r requirements.txt

For windows do
    cmd /c chcp 65001

Set password in __init__.py

run schema.sql
    psql -d kebab -U postgres -W -f loaddb.sql

Run Web-App
    python src/app.py