# Imports packages
from datetime import datetime
from math import radians, pi
import matplotlib.pyplot as plt
import os

import orekit
from orekit.pyhelpers import setup_orekit_curdir

# Initialises JVM and orekit library data
orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import TimeScalesFactory, AbsoluteDate
from org.orekit.utils import IERSConventions, Constants, PVCoordinatesProvider
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator

# Opens file directory to search for input TLE file
print(f"Files in Directory TLE")
for file_item in os.listdir("../../../TLE/TeLEOS-1"):
    print(file_item)
input_file_name = input("Input TLE file name with txt extension: ")
input_file_path = f"../../../TLE/TeLEOS-1/{input_file_name}"
print("Input file path:", input_file_path)

# Sets up TLE object
with open(input_file_path, "r") as file:
    next(file)
    file_content = file.read().splitlines()
    tle_line1 = file_content[0]
    tle_line2 = file_content[1]

tle_object = TLE(tle_line1, tle_line2)
print (tle_object)
print ('Epoch :',tle_object.getDate())

# Sets up frames, ground stations (Using GSC2)
ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, 
                         Constants.WGS84_EARTH_FLATTENING, 
                         ITRF)

latitude  = radians(1.29761) # degrees
longitude = radians(103.78036) # degrees
altitude  = 77.0 # metres
station = GeodeticPoint(latitude, longitude, altitude)
station_frame = TopocentricFrame(earth, station, "Esrange")
inertialFrame = FramesFactory.getEME2000()

# Sets up propagator for TLE
propagator = TLEPropagator.selectExtrapolator(tle_object)

# Sets up start and end time
extrapDate = AbsoluteDate(2025, 5, 10, 12, 0, 0.0, TimeScalesFactory.getUTC())
finalDate = extrapDate.shiftedBy(60.0*60*24) # seconds
step_size = 10.0 # seconds

# Sets up elevation 
az_el = []
pos = []

# Propagates TLE and generates values.
while extrapDate.compareTo(finalDate) <= 0.0:  
    # Propagates to set date time
    provider = PVCoordinatesProvider.cast_(propagator)

    # Generates PV object
    pv = provider.getPVCoordinates(extrapDate, inertialFrame)
    
    # Extracts PV values
    pos_tmp = pv.getPosition()
    pos.append((pos_tmp.getX(),pos_tmp.getY(),pos_tmp.getZ()))
    
    # Extracts azimuth and elevation values
    az_tmp = station_frame.getAzimuth(pos_tmp,
                    inertialFrame,
                    extrapDate)*180.0/pi # converts to degrees
    el_tmp = station_frame.getElevation(pos_tmp,
                    inertialFrame,
                    extrapDate)*180.0/pi # converts to degrees
    az_el.append((az_tmp, el_tmp))

    # Pushes date time forward by step_size
    extrapDate = extrapDate.shiftedBy(step_size)

# Plots for elevation and azimuth values
plt.plot(az_el)
plt.ylim(5, 360)
plt.title('Azimuth and Elevation')
plt.grid(True)
plt.show()