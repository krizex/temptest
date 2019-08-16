#!/bin/bash

if ! pip --version > /dev/null 2>&1; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
fi
pip install -r client-requirements.txt
