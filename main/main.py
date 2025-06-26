# Imports packages for initialisation
import csv
import os
from datetime import datetime
import orekit
from orekit.pyhelpers import setup_orekit_curdir

# Initialises JVM and orekit library data
orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

# Imports orekit library packages
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

# Assigns variables needed for data transformation
utc = TimeScalesFactory.getUTC()
inertial = FramesFactory.getTEME()
ecef = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
satellite = ObservableSatellite(0)
list_measurements = []

# Opens file directory to search for input csv file with measurement data
print(f"Files in Directory Teleos-1 WOD_proc")
input_file_directory = "../../Data/TELEOS_1/WOD_proc"
for file_item in os.listdir(input_file_directory):
    print(file_item)
input_file_name = input("Input data file name with csv extension: ")
input_file_path = f"{input_file_directory}/{input_file_name}"
print("Input file path:", input_file_path)

# Extracts, transforms and loads data
with open(input_file_path,"r") as file:
    file_content = csv.reader(file)
    next(file_content)
    for row in file_content:
        # Extracts and transforms date time
        datetime_str = row[0]
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
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

# Opens file directory to search for input TLE file
print(f"Files in Directory TLE")
for file_item in os.listdir("../../../TLE/TeLEOS-1"):
    print(file_item)
input_file_name = input("Input TLE file name with txt extension: ")
input_file_path = f"../../../TLE/TeLEOS-1/{input_file_name}"
print("Input file path:", input_file_path)

# Creates TLE initial guess
with open(input_file_path, "r") as file:
    next(file)
    file_content = file.read().splitlines()
    tle_line1 = file_content[0]
    tle_line2 = file_content[1]
tle_initial = TLE(tle_line1, tle_line2)
print("Initial TLE")
print(tle_initial)

# Creates TLE Propagator Builder
builder = TLEPropagatorBuilder(tle_initial, PositionAngleType.MEAN, 1.0, LeastSquaresTleGenerationAlgorithm())

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
print(tlepropagator_estimated_tle.getLine1())
print(tlepropagator_estimated_tle.getLine2())

# Output to new TLE txt document
output_file_path = input_file_path.replace("Spacetrack", "Orekit_TEME_PVT_1")
with open(output_file_path, "w") as file:
    file.write(f"TeLEOS-1\n{tlepropagator_estimated_tle.getLine1()}\n{tlepropagator_estimated_tle.getLine2()}")