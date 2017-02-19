import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


GOOGLE_JAVA_CODEFMT_URL = "https://github.com/google/google-java-format/releases/download/google-java-format-1.3/google-java-format-1.3-all-deps.jar"

RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)

@task
def install_deps(google_java_codefmt_url=GOOGLE_JAVA_CODEFMT_URL):
  apt.apt_install("make build-essential cmake python-dev python3-dev astyle pyflakes exuberant-ctags")
  with settings(warn_only=True):
    run("mkdir -p $HOME/software/jars")

  util.remote_file(google_java_codefmt_url, "$HOME/software/jars", backup=False)
  run("curl https://raw.githubusercontent.com/Shougo/neobundle.vim/master/bin/install.sh | sh")
