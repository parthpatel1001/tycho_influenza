#!/bin/bash
if ! command -v python3 &>/dev/null; then
    echo "python3 required"
    exit 1
fi

if ! command -v pip3 &>/dev/null; then
    echo "pip3 required";
    exit 1
fi

pip3 install virtualenv

if [ ! -d venv ]; then
	echo "venv not found, setting up"
	virtualenv venv
fi

mkdir -p data
source venv/bin/activate
pip3 install -r requirements.txt
echo 'Setup complete; run `source venv/bin/activate` to load environment'