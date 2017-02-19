import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"
MAVEN_URL = "http://mirrors.koehn.com/apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz"
ECLIPSE_URL = "http://mirror.cc.columbia.edu/pub/software/eclipse/technology/epp/downloads/release/neon/2/eclipse-java-neon-2-linux-gtk-x86_64.tar.gz"
ECLIM_URL = "https://github.com/ervandew/eclim/releases/download/2.6.0/eclim_2.6.0.jar"

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
  run("echo 'export JAVA_HOME=/usr/lib/jvm/java-8-oracle' >> $HOME/.bashrc")
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


@task
def install_eclim(eclipse_url=ECLIPSE_URL, eclim_url=ECLIM_URL):
  apt.apt_install("xvfb build-essential")
  with settings(warn_only=True):
    run("mkdir $HOME/software")

  eclipse_install_folder = "$HOME/software/eclipse"
  util.remote_archive(eclipse_url, eclipse_install_folder)

  eclim_install_folder = "$HOME/software/eclim"
  with settings(warn_only=True):
    run("mkdir %s" % eclim_install_folder)

  with cd(eclim_install_folder):
    run("wget %s" % eclim_url)

  run("java -Dvim.files=$HOME/.vim -Declipse.home=$HOME/software/eclipse -jar $HOME/software/eclim/eclim_2.6.0.jar install")
