import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *


RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)


"""
If you have VBoxGuestAdditions.iso specifiy as a parameter, 
otherwise virtualbox will be installed on the guest system.
To obtain my local copy of the iso, I through apt and copied it
http://www.virtualbox.org/manual/ch04.html
""" 
@task
def install_guest_additions(iso=None):
  user = util.env_var("$USER")
  apt.apt_install("dkms")
  reboot(180)
  guest_addition_mnt = "/mnt/vbox_guest_additions"

  if iso:
    guest_addition_iso = "/tmp/VBoxGuestAdditions.iso"
    util.remote_file(iso, guest_addition_iso)
  else:
    apt.apt_install("virtualbox-guest-additions")
    guest_addition_iso = "/usr/share/virtualbox/VBoxGuestAdditions.iso"

  sudo("mkdir -p %s" % guest_addition_mnt)
  sudo("mount -o loop %s %s" % (guest_addition_iso, guest_addition_mnt))
  with cd(guest_addition_mnt):
    sudo("./VBoxLinuxAdditions.run")

  sudo("umount %s" % guest_addition_mnt)
  sudo("rmdir %s" % guest_addition_mnt)
  sudo("usermod -a -G vboxsf %s" % user)
  print("you may need to logout and login for group changes to take effect")
