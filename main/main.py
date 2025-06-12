#import orekit
#orekit.initVM()

#from orekit.pyhelpers import setup_orekit_curdir
#setup_orekit_curdir(from_pip_library=True)

import sys
import os

# Add utils directory to sys.path temporarily
sys.path.append(os.path.abspath('main'))

import gps_data
print(gps_data.list_measurements)