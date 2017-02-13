import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)


@task
def setup():
  apt.apt_update()
  apt.apt_install("git git-flow")
  apt.apt_install("gcc g++")
  apt.apt_install("p7zip unzip")
  apt.apt_install("tmux")
  apt.apt_install("ntp")
  with settings(warn_only=True):
    run("mkdir $HOME/bin")


# for curses interfaces, <tab> to navigate, <space> to select
@task
def upgrade():
  apt.apt_update()
  apt.apt_upgrade()


@task
def authorize_sshkey(user=env.user, pub_ssh_key="~/.ssh/id_rsa.pub"):
  if not pub_ssh_key.endswith(".pub"):
    raise RuntimeError("public sshkey should end with .pub, for safety")

  with open(os.path.expanduser(pub_ssh_key), 'r') as f:
    pubkey = f.read().strip()

  with settings(warn_only=True):
    if user == env.user:
      run("mkdir $HOME/.ssh")
    else:
      sudo("mkdir /home/%s/.ssh" % user)

  if user == env.user:
    run("echo \"%s\" >> $HOME/.ssh/authorized_keys" % pubkey)
  else:
    sudo("echo \"%s\" >> /home/%s/.ssh/authorized_keys" % (pubkey,user))
    sudo("chown -R %s:%s /home/%s/.ssh" % (user,user,user))


# WARNING, this is more insecure, but allows automated provisioning
@task
def nopasswd_sudo(user, tmp_dir="/tmp"):
  tmp_file = tmp_dir + "/" + util.string_md5(user)
  sudo("echo '%s ALL=(ALL) NOPASSWD: ALL' > %s" % (user, tmp_file))
  util.chmod(tmp_file, "440", use_sudo=True)
  util.mv(tmp_file, "/etc/sudoers.d/%s" % user + "_fabric", use_sudo=True)


@task
def remove_nopasswd_sudo(user):
  sudo("rm /etc/sudoers.d/%s" % user + "_fabric")


@task
def run_cmd(cmd):
  util.run_cmd(cmd)


@task
def sudo_cmd(cmd):
  util.sudo_cmd(cmd)
