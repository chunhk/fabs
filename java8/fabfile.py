import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"
MAVEN_URL = "http://mirrors.koehn.com/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz"

apt = Apt(RESOURCE_PATH)


@task
def install():
  sudo("echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections")
  sudo("echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections")
  apt.add_apt_repository("ppa:webupd8team/java")
  apt.apt_update()
  apt.apt_install("oracle-java8-installer")
  setup_java_home()


@task
def setup_java_home():
  run("echo '' >> $HOME/.bashrc" )
  run("echo '# automatically added by setup_java_home' >> $HOME/.bashrc" )
  run("echo 'export JAVA_HOME=/usr/lib/jvm/java-7-oracle' >> $HOME/.bashrc")
  run("echo '# end' >> $HOME/.bashrc" )
  

@task
def install_maven(maven_url=MAVEN_URL):
  with settings(warn_only=True):
    run("mkdir $HOME/software")

  basename = os.path.basename(maven_url).replace("-bin.tar.gz", "")
  remote_name = "$HOME/software/" + basename
  util.remote_archive(maven_url, remote_name)

  with cd("$HOME/software"):
    run("ln -s %s apache-maven" % basename)

  with cd("$HOME/bin"):
    run("ln -s -f $HOME/software/apache-maven/bin/mvn .")

