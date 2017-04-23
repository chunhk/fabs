import hashlib
import os

from burlap import util
from burlap.apt import Apt
from fabric.api import *
from fabric.contrib import files
from functools import partial
from string import Template as StringTemplate


VIRTUAL_ENV = "$HOME/venv/pyml3"
RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/resources"

apt = Apt(RESOURCE_PATH)


@task
def install_all(virtualenv=VIRTUAL_ENV, upgrade=False, interactive=False):
  install_virtualenv(virtualenv)
  install_numpy(virtualenv, upgrade)
  install_scipy(virtualenv, upgrade)
  install_matplotlib(virtualenv, upgrade)
  install_pandas(virtualenv, upgrade)
  install_statsmodels(virtualenv, upgrade)
  install_pytables(virtualenv, upgrade)
  install_scikit_learn(virtualenv, upgrade)
  install_nltk(virtualenv, upgrade)
  install_ipython(virtualenv, upgrade)
  if interactive:
    install_ipython_notebook(virtualenv, upgrade)
  else:
    print("running in non-interactive mode, ipython notebook not installed")


@task
def is_virtualenv_installed(virtualenv=VIRTUAL_ENV):
  if virtualenv_installed():
    print("virtual env exists: ", VIRTUAL_ENV)
    return True
  else:
    print("virtual env does not exist: ", VIRTUAL_ENV)
    return False


@task
def install_virtualenv(virtualenv=VIRTUAL_ENV):
  if not is_virtualenv_installed():
    run("python3 -m venv %s" % VIRTUAL_ENV)
    pip_install(virtualenv, "pip", upgrade=True)


@task
def installed_site_packages(virtualenv=VIRTUAL_ENV):
  pip(virtualenv, "freeze")

 
@task
def install_base(virtualenv=VIRTUAL_ENV):
  apt.apt_install("gcc g++ python3-dev")


@task
def install_numpy(virtualenv=VIRTUAL_ENV, upgrade=False):
  install_base()
  pip_install(virtualenv, "numpy", upgrade=upgrade)


@task
def install_scipy(virtualenv=VIRTUAL_ENV, upgrade=False):
  install_base()
  apt.apt_install("libblas-dev liblapack-dev libatlas-dev gfortran")
  pip_install(virtualenv, "scipy", upgrade=upgrade)


@task
def install_pandas(virtualenv=VIRTUAL_ENV, upgrade=False):
  install_base()
  pip_install(virtualenv, "pandas", upgrade=upgrade)


@task
def install_statsmodels(virtualenv=VIRTUAL_ENV, upgrade=False):
  install_base()
  pip_install(virtualenv, "statsmodels", upgrade=upgrade)


@task
def install_pytables(virtualenv=VIRTUAL_ENV, upgrade=False):
  install_base()
  apt.apt_install("libhdf5-10 libhdf5-dev libhdf5-doc")
  pip_install(virtualenv, "numexpr", upgrade=upgrade)
  pip_install(virtualenv, "cython", upgrade=upgrade)
  pip_install(virtualenv, "tables", upgrade=upgrade)


@task
def install_scikit_learn(virtualenv=VIRTUAL_ENV, upgrade=False):
  install_base()
  pip_install(virtualenv, "scikit-learn", upgrade=upgrade)


@task
def install_matplotlib(virtualenv=VIRTUAL_ENV, upgrade=False):
  install_base()
  apt.apt_install("libfreetype6 libfreetype6-dev libpng12-0 libpng12-dev")
  pip_install(virtualenv, "matplotlib", upgrade=upgrade)


@task
def install_ipython(virtualenv=VIRTUAL_ENV, upgrade=False):
  pip_install(virtualenv, "ipython", upgrade=upgrade)


"""
IPython Notebook
http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html 
http://ipython.org/ipython-doc/dev/install/install.html#installnotebook
"""

ipython_nb_root = "$HOME/.ipython3_nb"
ipython_nb_pid = "%s/pid" % ipython_nb_root
ipython_nb_cert = "%s/mycert.pem" % ipython_nb_root
ipython_nb_log = "%s/log" % ipython_nb_root
ipython_nb_notebook_path = "$HOME/ipython3_notebooks"
ipython_nb_bin = "$HOME/bin/ipython3_notebook"
ipython_config = "%s/ipython_notebook_config.py" % ipython_nb_root

@task
def install_ipython_notebook(virtualenv=VIRTUAL_ENV, upgrade=False):
  apt.apt_install("libzmq1 libzmq-dev libzmq-dbg")
  pip_install(virtualenv, "tornado", upgrade=upgrade)
  pip_install(virtualenv, "pyzmq", upgrade=upgrade)
  pip_install(virtualenv, "jupyter", upgrade=upgrade)
  pip_install(virtualenv, "ipykernel", upgrade=upgrade)
  run("%s/bin/python -m ipykernel install --user --name pyml3" % virtualenv)
  setup_ipython_nb_paths()
  setup_ipython_scripts(virtualenv)
  configure_ipython_notebook()


def setup_ipython_nb_paths():
  with settings(warn_only=True):
    run("mkdir %s" % ipython_nb_root)
    run("mkdir %s" % ipython_nb_notebook_path)


def setup_ipython_scripts(virtualenv=VIRTUAL_ENV, port=8987):
  util.remote_template(RESOURCE_PATH + "/ipython_notebook.jinja2", \
      variables={"virtualenv": virtualenv, "port": port, \
      "logfile": ipython_nb_log, "pidfile": ipython_nb_pid,
      "config": ipython_config}, \
      dest_file=ipython_nb_bin, permissions="+x")


def configure_ipython_notebook(virtualenv=VIRTUAL_ENV):
  if not files.exists(ipython_config):
    home_path = util.home_path()
    run("openssl req -x509 -nodes -days 1095 -newkey rsa:1024 -keyout %s -out %s" % (ipython_nb_cert, ipython_nb_cert))

    run("echo \"c.NotebookApp.certfile = u'%s'\" >> %s" % \
        (StringTemplate(ipython_nb_cert).substitute(HOME=home_path), \
        ipython_config))

    # Change to localhost if you want to keep it private.
    run("echo \"c.NotebookApp.ip = '0.0.0.0'\" >> %s" % ipython_config)
    run("echo \"c.NotebookApp.open_browser = False\" >> %s" % ipython_config)
    run("echo \"c.NotebookApp.notebook_dir = u'%s'\" >> %s" % \
        (StringTemplate(ipython_nb_notebook_path).substitute(HOME=home_path), \
        ipython_config))

    python_path = StringTemplate(virtualenv + "/bin/python").substitute( \
        HOME=home_path)
    ipython_config_path = StringTemplate(ipython_config).substitute( \
        HOME=home_path)

    util.run_remote_template(RESOURCE_PATH + "/ipython_passwd.py", \
        variables={"python_path": python_path, \
        "ipython_config": ipython_config_path})


@task
def ipython_start(virtualenv=VIRTUAL_ENV):
  run(ipython_nb_bin + " start", pty=False)


@task
def ipython_stop(virtualenv=VIRTUAL_ENV):
  run(ipython_nb_bin + " stop")


@task
def ipython_status(virtualenv=VIRTUAL_ENV):
  run(ipython_nb_bin + " status")

@task
def install_nltk(virtualenv=VIRTUAL_ENV, upgrade=False):
  pip_install(virtualenv, "pyyaml", upgrade=upgrade)
  pip_install(virtualenv, "nltk", upgrade=upgrade)

@task
def install_tensorflow(virtualenv=VIRTUAL_ENV):
  pip_install(virtualenv, "numpy", upgrade=True)
  pip_install(virtualenv, "wheel", upgrade=True)
  pip_install(virtualenv, "six", upgrade=True)

  if not files.exists("$HOME/dev/tensorflow/configure"):
    with cd("$HOME/dev"):
      run("git clone https://github.com/tensorflow/tensorflow")

  with cd("$HOME/dev/tensorflow"):
    run("git checkout r1.1")
    run("bazel clean")
    run("./configure")
    run("bazel build --config=opt //tensorflow/tools/pip_package:build_pip_package")
    run("bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg")
    pip_install(virtualenv, "/tmp/tensorflow_pkg/tensorflow-1.1.0-cp35-cp35m-linux_x86_64.whl")


"""
Helper Functions
"""

def virtualenv_installed(virtualenv=VIRTUAL_ENV):
  return files.exists("%s/bin/activate" % virtualenv)


def pip(virtualenv, cmd):
  run("%s/bin/pip %s" % (virtualenv, cmd))


def pip_install(virtualenv, package, upgrade=False):
  cmd = "install -U %s" % package if upgrade else "install %s" % package
  pip(virtualenv, cmd)