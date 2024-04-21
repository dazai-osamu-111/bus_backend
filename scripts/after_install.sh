#!/usr/bin/env bash

# kill any servers that may be running in the background 
# sudo pkill -f runserver

# # kill frontend servers if you are deploying any frontend
# # sudo pkill -f tailwind
# # sudo pkill -f node

# cd /home/ubuntu/bus_backend/

# # activate virtual environment
# python3 -m venv venv
# source venv/bin/activate

# install requirements.txt
# pip install -r /home/ubuntu/bus_backend/requirements.txt

# # run server
# screen -d -m python3 manage.py runserver 0:8000


echo "[$(date)] Changing directory to /home/ubuntu/bus_backend/"
cd /home/ubuntu/bus_backend/

echo "[$(date)] Activating virtual environment..."
# python -m venv venv
source venv/bin/activate

echo "[$(date)] Installing requirements from requirements.txt..."
# pip install -r /home/ubuntu/bus_backend/requirements.txt

echo "[$(date)] Starting server in detached screen..."
screen -d -m python manage.py runserver 0:8000

echo "[$(date)] Deployment script finished."