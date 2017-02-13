import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


LEIN_URL = "https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein"
VERTX_URL = "https://bintray.com/artifact/download/vertx/downloads/vert.x-3.3.3-full.tar.gz"

RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)


# press up and down to scroll and q during rvm ruby install
@task
def install_rvm(install_ruby_version=None):
  run("gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3")
  run("\curl -sSL https://get.rvm.io | bash -s stable")

  apt.apt_install("build-essential openssl libreadline6 libreadline6-dev curl git zlib1g zlib1g-dev libssl-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt-dev autoconf libc6-dev ncurses-dev automake libtool bison subversion pkg-config")
  
  if install_ruby_version:
    run("rvm install %s" % install_ruby_version)


@task
def install_lein():
  with settings(warn_only=True):
    run("mkdir $HOME/bin")

  with cd("$HOME/bin"):
    run("wget %s -O lein" % LEIN_URL)
    util.chmod("$HOME/bin/lein", "+x")


@task
def install_haskell():
  apt.apt_install("ghc haskell-platform haskell-stack cabal-install")


@task
def install_golang():
  apt.add_apt_repository("ppa:ubuntu-lxc/lxd-stable")
  apt.apt_update()
  apt.apt_install("golang")


@task
def install_nodejs():
  sudo("curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -")
  apt.apt_update()
  apt.apt_install("nodejs")


@task
def install_sbt():
  sudo("echo \"deb https://dl.bintray.com/sbt/debian /\" | sudo tee -a /etc/apt/sources.list.d/sbt.list")
  sudo("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823")
  apt.apt_update()
  apt.apt_install("sbt")


@task
def install_giter8():
  run("curl https://raw.github.com/n8han/conscript/master/setup.sh | sh")
  run("cs n8han/giter8")


@task
def install_vertx(vertx_url=VERTX_URL):
  with settings(warn_only=True):
    run("mkdir $HOME/software")
    run("mkdir $HOME/bin")

  basename = os.path.basename(vertx_url).replace(".tar.gz", "")
  install_folder = "$HOME/software/%s" % basename
  util.remote_archive(vertx_url, install_folder)

  with cd("$HOME/software"):
    run("ln -s %s %s" % (basename, "vertx"))

  with cd("$HOME/bin"):
    run("ln -s %s ." % "$HOME/software/vertx/bin/vertx")


@task
def install_octave():
  apt.apt_install("octave octave-info octave-doc")


@task
def diff(local_file, remote_file):
  with settings(warn_only=True):
    local("/bin/bash -c \"diff %s <(ssh %s %s@%s 'cat %s')\"" % \
        (local_file, ("-i %s" % env.key_filename[0] if env.key_filename else ""), env.user, env.host, remote_file))


@task
def dir_cmp(local_dir, remote_dir):
  local('rsync -rvnc --delete -e "ssh %s" %s@%s:%s %s' %
      (("-i %s" % env.key_filename[0] if env.key_filename else ""), env.user, env.host, remote_dir, local_dir))


@task
def install_drake():
  with cd("$HOME/software"):
    run("git clone git://github.com/Factual/drake.git")

  with cd("$HOME/software/drake"):
    run("lein uberjar")

  util.remote_file(RESOURCE_PATH + "/drake", "$HOME/bin", backup=False,
      permissions="755")


@task
def install_bazel():
  sudo("echo \"deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8\" | sudo tee /etc/apt/sources.list.d/bazel.list")
  sudo("curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -")
  apt.apt_update()
  apt.apt_install("bazel")


@task
def install_docker():
  docker_apt_repo_file = "docker.list"
  if not apt.check_apt_repo(docker_apt_repo_file):
    sudo("sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D")
    apt.install_apt_repo(docker_apt_repo_file)
    apt.apt_update()
  else:
    print "apt repo %s already exists" % docker_apt_repo_file

  run("apt-cache policy docker-engine")
  apt.apt_install("docker-engine")
