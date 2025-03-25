#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Virtual environment is ready. Use 'source venv/bin/activate' to activate it."
