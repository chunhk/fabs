from functools import partial
import os

from fabric.api import *
from fabric.contrib import files

from burlap import util
from burlap.apt import Apt


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)
name = "monit"

@task
def installed():
  if is_installed():
    print "%s is installed" % name
  else:
    print "%s is not installed" % name

@task
def install():
  if not is_installed():
    apt.apt_install("monit")
    update_config()
    restart()
  else:
    print "%s already installed" % name

@task
def update_config():
  put(RESOURCE_PATH + "/monitrc", "/etc/monit", use_sudo=True)
  sudo("chown root:root /etc/monit/monitrc")

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

@task
def reload():
  control(cmd="reload")

control = partial(util.initd_control, script="monit")

def is_installed():
  return files.exists("/etc/init.d/monit")
