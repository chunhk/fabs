from functools import partial

from fabric.api import *
from fabric.contrib import files

from burlap import apt, util

name = "r"
apt_repo_file = "cran.list"
rstudio_url = "http://download2.rstudio.org/rstudio-server-0.97.247-amd64.deb"

@task
def check_apt_repo():
  apt.check_apt_repo_task(apt_repo_file)

@task
def install_apt_repo():
  if not apt.check_apt_repo(apt_repo_file):
    sudo("sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9")
    apt.install_apt_repo(apt_repo_file)
    apt.apt_update()
  else:
    print "apt repo %s already exists" % apt_repo_file
 
@task
def installed():
  if is_installed():
    print "%s is installed" % name
  else:
    print "%s is not installed" % name

@task
def install():
  if not is_installed():
    install_apt_repo()
    apt.apt_install("r-recommended")
    apt.apt_install("r-base-dev")
  else:
    print "%s is already installed!" % name

@task
def install_rstudio():
  rstudio_file = "/tmp/" + rstudio_url.split("/")[-1]
  apt.apt_install("gdebi-core")
  apt.apt_install("libapparmor1")
  sudo("wget -O %s %s" % (rstudio_file, rstudio_url))
  sudo("gdebi -n %s" % rstudio_file)
  print "rstudio default port is 8787"

@task
def status():
  rstudio_control(cmd="status")

@task
def start():
  rstudio_control(cmd="start")

@task
def stop():
  rstudio_control(cmd="stop")

@task
def restart():
  rstudio_control(cmd="restart")

rstudio_control = partial(util.upstart_control, service="rstudio-server")

def is_installed():
  return files.exists("/usr/bin/R")

def is_rstudio_installed():
  return True
