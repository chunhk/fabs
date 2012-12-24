import os

from fabric.api import *

from burlap.apt import Apt


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)

@task
def install():
  sudo("echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections")
  sudo("echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections")
  apt.add_apt_repository("ppa:webupd8team/java")
  apt.apt_update()
  apt.apt_install("oracle-java7-installer")
