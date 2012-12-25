import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"
MAVEN_URL = "http://apache.cs.utah.edu/maven/maven-3/3.0.4/binaries/apache-maven-3.0.4-bin.tar.gz"

apt = Apt(RESOURCE_PATH)


@task
def install():
  sudo("echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections")
  sudo("echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections")
  apt.add_apt_repository("ppa:webupd8team/java")
  apt.apt_update()
  apt.apt_install("oracle-java7-installer")
  

@task
def install_maven():
  with settings(warn_only=True):
    run("mkdir $HOME/software")

  util.remote_archive(MAVEN_URL, "$HOME/software/apache-maven")

  with cd("$HOME/bin"):
    run("ln -s -f $HOME/software/apache-maven/bin/mvn .")

