import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir
setup_orekit_curdir(from_pip_library=True)

from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import TimeScalesFactory, AbsoluteDate, DateComponents, TimeComponents
from org.orekit.utils import IERSConventions, Constants, PVCoordinatesProvider

from org.orekit.propagation.analytical.tle import TLE, TLEPropagator

from math import radians, pi
import matplotlib.pyplot as plt

#SPOT-5 
tle_line1 = "1 27421U 02021A   02124.48976499 -.00021470  00000-0 -89879-2 0    20"
tle_line2 = "2 27421  98.7490 199.5121 0001333 133.9522 226.1918 14.26113993    62"

mytle = TLE(tle_line1,tle_line2)

print (mytle)
print ('Epoch :',mytle.getDate())

ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, 
                         Constants.WGS84_EARTH_FLATTENING, 
                         ITRF)

longitude = radians(21.063)
latitude  = radians(67.878)
altitude  = 341.0
station = GeodeticPoint(latitude, longitude, altitude)
station_frame = TopocentricFrame(earth, station, "Esrange")

inertialFrame = FramesFactory.getEME2000()
propagator = TLEPropagator.selectExtrapolator(mytle)

extrapDate = AbsoluteDate(2002, 5, 7, 12, 0, 0.0, TimeScalesFactory.getUTC())
finalDate = extrapDate.shiftedBy(60.0*60*24) #seconds

el=[]
pos=[]

while extrapDate.compareTo(finalDate) <= 0.0:  
    provider = PVCoordinatesProvider.cast_(propagator)
    pv = provider.getPVCoordinates(extrapDate, inertialFrame)
    pos_tmp = pv.getPosition()
    pos.append((pos_tmp.getX(),pos_tmp.getY(),pos_tmp.getZ()))
    
    el_tmp = station_frame.getElevation(pv.getPosition(),
                    inertialFrame,
                    extrapDate)*180.0/pi
    el.append(el_tmp)
    #print extrapDate, pos_tmp, vel_tmp
    extrapDate = extrapDate.shiftedBy(10.0)

plt.plot(el)
plt.ylim(0,90)
plt.title('Elevation')
plt.grid(True)
plt.show()

plt.plot(pos)
plt.title('Inertial position')