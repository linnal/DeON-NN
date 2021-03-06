# !/bin/bash

set -e

PYTHON=python3
VENV_DIR=.venv
REQUIREMENTS=requirements.txt
DEVICE=$1
TF_VERSION='tensorflow'

if [[ $1 == 'gpu' ]]; then
    TF_VERSION='tensorflow-gpu'
else
    TF_VERSION='tensorflow'
fi

# if .py3venv doesn't exists, create it,
# otherwise activate the virtual environment
if [ -d $VENV_DIR ]; then
    echo $VENV_DIR 'already exists: deleting.'
    rm -rf $VENV_DIR
fi

# else
echo 'creating virtual env...'
virtualenv $VENV_DIR --python=$PYTHON
source $VENV_DIR/bin/activate
echo 'installing tensorflow version: '$TF_VERSION
pip install $TF_VERSION==1.3.0
pip install -r $REQUIREMENTS --process-dependency-links
echo 'removing *.egg-info directory'
rm -rf *.egg-info
echo 'done'
deactivate
