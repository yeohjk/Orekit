import csv
from datetime import datetime
import orekit
from orekit.pyhelpers import setup_orekit_curdir
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.frames import FramesFactory
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.utils import Constants, PVCoordinates, ParameterDriver
from org.orekit.models.earth import ReferenceEllipsoid
#from org.orekit.propagation.analytical.tle import TLE, TLEPropagatorBuilder
from org.orekit.estimation.leastsquares import BatchLSEstimator
from org.orekit.estimation.measurements import PV
#from org.orekit.estimation.measurements.modifiers import OnBoardAntennaRangeModifier
from org.orekit.estimation.measurements import ObservableSatellite
from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.hipparchus.optim.nonlinear.vector.leastsquares import LevenbergMarquardtOptimizer


orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

utc = TimeScalesFactory.getUTC()

with open("data/WOD_GPS_Test_Data_ 100525.csv","r") as file:
    file_content = csv.reader(file)
    next(file_content)
    for row in file_content:
        datetime_str = row[0]
        datetime_obj = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
        print(datetime_obj)
