import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *
from fabric.contrib import files
from functools import partial


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)
name = "zookeeper"
apt_repo_file = "cloudera.list"
control = partial(util.initd_control, script="hadoop-zookeeper-server")


@task
def check_apt_repo():
  apt.check_apt_repo_task(apt_repo_file)


@task
def install_apt_repo():
  if not apt.check_apt_repo(apt_repo_file):
    sudo("curl -s http://archive.cloudera.com/debian/archive.key | sudo apt-key add -")
    apt.install_apt_repo(apt_repo_file)
  else:
    print("apt repo %s already exists" % apt_repo_file)

 
@task
def installed():
  if is_installed():
    print("%s is installed" % name)
    return True
  else:
    print("%s is not installed" % name)
    return False


@task
def install():
  if not is_installed():
    install_apt_repo()
    apt.apt_install("hadoop-zookeeper")
    apt.apt_install("hadoop-zookeeper-server")
    update_config()
    restart()


@task
def update_config():
  util.remote_file(RESOURCE_PATH + "/zoo.cfg", "/etc/zookeeper", \
      use_sudo=True, owner="root", group="root")


@task
def status():
  control(cmd="status")


@task
def start():
  control(cmd="start")


@task
def stop():
  control(cmd="stop")


@task
def restart():
  control(cmd="restart")


def is_installed():
  return files.exists("/etc/init.d/hadoop-zookeeper-server")
