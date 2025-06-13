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
from org.orekit.propagation.analytical.tle import TLE
from org.orekit.propagation.conversion import TLEPropagatorBuilder

# Initialises JVM and orekit library data
orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

# Setting variables needed for data transformation
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
        # Extracting and transforming date time
        datetime_str = row[0]
        datetime_obj = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
        year, month, day = datetime_obj.year, datetime_obj.month, datetime_obj.day
        hour, minute, second = datetime_obj.hour, datetime_obj.minute, float(datetime_obj.second)
        abs_date = AbsoluteDate(year, month, day, hour, minute, second, utc)
        # Extracting and transforming position and velocity from non-inertial ITRF ECEF frame to inertial EME2000 frame
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
print(list_measurements)

# Creating TLE initial guess
tle_line1 = "1 00005U 58002B   20062.53480374  .00000023  00000-0  28098-4 0  9991"
tle_line2 = "2 00005  34.2682 348.7242 1849677 331.7664  19.3264 10.82419157413667"
tle_initial = TLE(tle_line1, tle_line2)
print(tle_initial)


