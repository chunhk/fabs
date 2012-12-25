import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)


@task
def setup():
  apt.apt_update()
  apt.apt_install("python-software-properties")
  apt.apt_install("python-virtualenv")
  apt.apt_install("git git-flow")
  apt.apt_install("gcc g++")
  apt.apt_install("p7zip unzip")
  with settings(warn_only=True):
    run("mkdir $HOME/bin")


@task
def upgrade():
  apt.apt_upgrade()

  
@task
def authorize_sshkey(pub_ssh_key="~/.ssh/id_rsa.pub"):
  with open(os.path.expanduser(pub_ssh_key), 'r') as f:
    pubkey = f.read()

  with settings(warn_only=True):
    run("mkdir $HOME/.ssh")

  run("echo \"%s\" >> $HOME/.ssh/authorized_keys" % pubkey)


@task
def run_cmd(cmd):
  util.run_cmd(cmd)


@task
def sudo_cmd(cmd):
  util.sudo_cmd(cmd)
