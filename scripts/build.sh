#!/bin/bash

git pull

source venv/bin/activate
pip install -r requirements.txt

./src/manage.py migrate
./src/manage.py collectstatic --noinput

sudo supervisorctl restart hotel_pro_uwsgi

# sudo service nginx restart
