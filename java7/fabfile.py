from fabric.api import *

from burlap import apt

def install():
  sudo("echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections")
  sudo("echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections")
  apt.add_apt_repository("ppa:webupd8team/java")
  apt.apt_update()
  apt.apt_install("oracle-java7-installer")
