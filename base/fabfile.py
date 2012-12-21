from fabric.api import *

from burlap import apt,util

@task
def setup():
  apt.apt_update()
  apt.apt_install("python-software-properties")
  apt.apt_install("git")
  apt.apt_install("gcc g++")

@task
def run_cmd(cmd):
  util.run_cmd(cmd)

@task
def sudo_cmd(cmd):
  util.sudo_cmd(cmd)
