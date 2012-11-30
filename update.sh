#!/bin/sh

home_dir=env
python virtualenv.py $home_dir
source $home_dir/bin/activate
pip install -r requirements.txt
python update.py "$@"
