#!/bin/bash
set -e

VENV_ROOT=~/venv
VENV=$VENV_ROOT/fabric-venv

sudo apt-get install python python-dev python-virtualenv
mkdir -p $VENV_ROOT
virtualenv $VENV
$VENV/bin/pip install --upgrade pip
$VENV/bin/pip install fabric
$VENV/bin/pip install git+git://github.com/chunhk/burlap.git
