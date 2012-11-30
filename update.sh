#!/bin/sh

env_home_dir=env
echo $env_home_dir
python virtualenv.py $env_home_dir
source $env_home_dir/bin/activate
pip install -r requirements.txt
python update.py "$@"
