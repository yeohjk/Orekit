import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir, absolutedate_to_datetime
setup_orekit_curdir(from_pip_library=True)

from org.hipparchus.geometry.euclidean.threed import Vector3D, SphericalCoordinates
from org.orekit.data import DataProvidersManager, ZipJarCrawler
from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint, CelestialBodyFactory
from org.orekit.time import TimeScalesFactory, AbsoluteDate, DateComponents, TimeComponents
from org.orekit.utils import IERSConventions, Constants, PVCoordinates, PVCoordinatesProvider, AbsolutePVCoordinates

from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from java.io import File

from math import radians, pi, degrees
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Testing Sun rotating frame and getParent() method
sun_frame = CelestialBodyFactory.getSun().getBodyOrientedFrame()
print(sun_frame, '\n',
      sun_frame.getParent(), '\n',
      sun_frame.getParent().getParent(), '\n',
      sun_frame.getParent().getParent().getParent(), '\n',
      sun_frame.getParent().getParent().getParent().getParent(),'\n',
     )

# Testing ICRF inertial reference frame and getParent() method
icrf_frame = FramesFactory.getICRF()
print(icrf_frame.getParent().getParent())

# Testing PV coordinate generation
eme_frame = FramesFactory.getEME2000()
position = Vector3D(3220103., 69623., 6449822.)
velocity = Vector3D(6414.7, -2006., -3180.)
pv_eme = PVCoordinates(position, velocity)
initDate = AbsoluteDate.J2000_EPOCH.shiftedBy(584.)
print(pv_eme)

# Testing ITRF and coordinate transform
ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
print(ITRF)
p2 = eme_frame.getTransformTo(ITRF, initDate).transformPVCoordinates(pv_eme)
print(p2)
p3 = ITRF.getTransformTo(eme_frame, initDate).transformPVCoordinates(p2)
print(p3)