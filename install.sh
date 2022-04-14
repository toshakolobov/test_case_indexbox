#!/bin/bash

python2 -m pip install virtualenv
python2 -m virtualenv --python=python2 venv
source venv/bin/activate

python2 -m pip install -r requirements.txt
