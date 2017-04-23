#!/bin/bash
set -e

VENV_ROOT=~/venv
VENV=$VENV_ROOT/fabric3-venv

sudo apt-get install python3 python3-dev python3-venv
mkdir -p $VENV_ROOT
python3 -m venv $VENV
$VENV/bin/pip install --upgrade pip
$VENV/bin/pip install fabric3
$VENV/bin/pip install git+git://github.com/chunhk/burlap.git@python3
