# Imports packages
import csv
from datetime import datetime
import orekit
from orekit.pyhelpers import setup_orekit_curdir
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.frames import FramesFactory
from org.orekit.utils import PVCoordinates, IERSConventions
from org.orekit.estimation.measurements import PV, ObservableSatellite
from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
from org.orekit.propagation.conversion import TLEPropagatorBuilder
from org.orekit.orbits import PositionAngleType
from org.orekit.propagation.analytical.tle.generation import LeastSquaresTleGenerationAlgorithm
from org.hipparchus.optim.nonlinear.vector.leastsquares import LevenbergMarquardtOptimizer
from org.orekit.estimation.leastsquares import BatchLSEstimator

# Initialises JVM and orekit library data
orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

# Sets variables needed for data transformation
utc = TimeScalesFactory.getUTC()
inertial = FramesFactory.getEME2000()
ecef = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
satellite = ObservableSatellite(0)
list_measurements = []

# Extracts, transforms and loads data
with open("data/WOD_GPS_Test_Data_ 100525.csv","r") as file:
    file_content = csv.reader(file)
    next(file_content)
    for row in file_content:
        # Extractsand transforms date time
        datetime_str = row[0]
        datetime_obj = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
        year, month, day = datetime_obj.year, datetime_obj.month, datetime_obj.day
        hour, minute, second = datetime_obj.hour, datetime_obj.minute, float(datetime_obj.second)
        abs_date = AbsoluteDate(year, month, day, hour, minute, second, utc)
        # Extracts and transforms position and velocity from non-inertial ITRF ECEF frame to inertial EME2000 frame
        pos_x, pos_y, pos_z = float(row[1]), float(row[2]), float(row[3])
        position = Vector3D(pos_x, pos_y, pos_z)
        vel_x, vel_y, vel_z = float(row[4]), float(row[5]), float(row[6])
        velocity = Vector3D(vel_x, vel_y, vel_z)
        pv_ecef = PVCoordinates(position, velocity)
        transform = ecef.getTransformTo(inertial, abs_date)
        pv_inertial = transform.transformPVCoordinates(pv_ecef)
        # Loads transformed data to list
        measurement = PV(abs_date, pv_inertial.getPosition(), pv_inertial.getVelocity(), 1.0, 1.0, 1.0, satellite)
        list_measurements.append(measurement)

# Creates TLE initial guess
with open("../../../TLE/TeLEOS-1/TLE TeLEOS-1 20250509 Spacetrack.txt", "r") as file:
    next(file)
    file_content = file.readlines()
    tle_line1 = file_content[0][:-1]
    tle_line2 = file_content[1]
tle_initial = TLE(tle_line1, tle_line2)
print("Initial TLE")
print(tle_initial)

# Creates TLE Propagator Builder
builder = TLEPropagatorBuilder(tle_initial, PositionAngleType.TRUE, 1.0, LeastSquaresTleGenerationAlgorithm())

# Creates optimizer and estimator
estimator = BatchLSEstimator(LevenbergMarquardtOptimizer(), builder)
for measurement in list_measurements:
    estimator.addMeasurement(measurement)
estimator.setMaxIterations(100)
estimator.setMaxEvaluations(1000)

# Estimates new TLE based on measurement data
propagator_estimated_tle = estimator.estimate()[0]
tlepropagator_estimated_tle = TLEPropagator.cast_(propagator_estimated_tle).getTLE()
print("Revised TLE")
print(tlepropagator_estimated_tle)



