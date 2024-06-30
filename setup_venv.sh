#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment and install dependencies
if [ "$OS" == "Windows_NT" ]; then
    . venv/Scripts/Activate.ps1
else
    source venv/bin/activate
fi

pip install -r requirements.txt