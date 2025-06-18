# Imports packages
from datetime import datetime
import orekit
from orekit.pyhelpers import setup_orekit_curdir

from org.orekit.frames import FramesFactory
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator

# Initialises JVM and orekit library data
orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

# Sets up TLE object
with open("../../../TLE/TeLEOS-1/TLE TeLEOS-1 20250509 Orekit_TEME_0.5.txt", "r") as file:
    next(file)
    file_content = file.readlines()
    print(file_content)
    tle_line1 = file_content[0][:-1]
    tle_line2 = file_content[1]

tle_object = TLE(tle_line1, tle_line2)
print (tle_object)
print ('Epoch :',tle_object.getDate())
