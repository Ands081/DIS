# DIS

Run the code below to install the dependencies.
    pip install -r requirements.txt

For windows do
    cmd /c chcp 65001

Set password in __init__.py

run loaddb.sql
    psql -d kebab -U postgres -W -f src/loaddb.sql
    psql -d kebab -U postgres -W -f src/loadreviews.sql

Run Web-App
    python src/app.py