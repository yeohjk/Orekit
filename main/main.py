# Imports gps_data
import sys
import os
sys.path.append(os.path.abspath('main'))
import gps_data
print(gps_data.list_measurements)

# Imports packages for orekit
import orekit
from orekit.pyhelpers import setup_orekit_curdir

# Initialises JVM and orekit library data
orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

