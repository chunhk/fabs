#!{{ python_path }}

import sys

from IPython.lib import passwd

pw_hash = passwd()

with open("{{ ipython_config }}", "a") as f:
  f.write("c.NotebookApp.password = u'%s'" % pw_hash)
