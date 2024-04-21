#!/usr/bin/env bash

sudo chown -R ubuntu:ubuntu ~/bus_backend
virtualenv /home/ubuntu/bus_backend/venv
source /home/ubuntu/bus_backend/venv/bin/activate
pip install -r /home/ubuntu/bus_backend/requirements.txt