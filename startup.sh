#!/bin/bash

# Create virtual environment
python -m venv /home/site/wwwroot/antenv

# Activate virtual environment
source /home/site/wwwroot/antenv/bin/activate

# Install dependencies
pip install -r /home/site/wwwroot/requirements.txt

# Run your app
gunicorn --bind 0.0.0.0:8080 app:app