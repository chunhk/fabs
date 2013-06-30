import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"
apt = Apt(RESOURCE_PATH)


@task
def install_rethinkdb():
  apt.add_apt_repository("ppa:rethinkdb/ppa")
  apt.apt_update()
  apt.apt_install("rethinkdb")


@task
def install_hyperdex():
  sudo("wget -O - http://ubuntu.hyperdex.org/hyperdex.gpg.key | apt-key add -")
  sudo("wget -O /etc/apt/sources.list.d/hyperdex.list http://ubuntu.hyperdex.org/hyperdex.list")
  apt.apt_update()
  apt.apt_install("hyperdex")


@task
def install_mongodb():
  sudo("apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10")
  sudo("echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/10gen.list")
  apt.apt_update()
  apt.apt_install("mongodb-10gen")
