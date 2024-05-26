#!/bin/bash
source config.sh
apt-get update -y
apt-get install python3 -y
apt-get install python3-venv -y
apt-get install postgresql -y
sudo -u postgres createuser $DB_USERNAME
sudo -u postgres createdb orderup
sudo -u postgres psql -d orderup -c "ALTER USER $DB_USERNAME WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -d orderup -c "ALTER DATABASE orderup OWNER TO $DB_USERNAME;"
cd backend
python3 -m venv env
source env/bin/activate
source ../config.sh
pip3 install -r requirements.txt
python3 init_db.py
python3 init_data.py
flask run
