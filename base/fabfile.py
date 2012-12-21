from fabric.api import *

from burlap import util

@task
def setup():
  sudo("apt-get install python-software-properties")
  sudo("apt-get install git")

@task
def run_cmd(cmd):
  util.run_cmd(cmd)

@task
def sudo_cmd(cmd):
  util.sudo_cmd(cmd)
