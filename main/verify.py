# Imports packages for initialisation
from datetime import datetime
from math import radians, pi
import matplotlib.pyplot as plt
import os
import orekit
from orekit.pyhelpers import setup_orekit_curdir

# Initialises JVM and orekit library data
orekit.initVM()
setup_orekit_curdir(from_pip_library=True)

# Imports orekit library packages
from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import TimeScalesFactory, AbsoluteDate
from org.orekit.utils import IERSConventions, Constants, PVCoordinatesProvider
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator

# Creates class verify_tle:
class verify_tle():
    def __init__(self):
        self.setup_frames()
        self.setup_gsc()
        self.setup_datetime()
        self.setup_tle()
        self.propagation()
        self.plots()
        return
    def setup_frames(self):
        # Sets up frames
        self.ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        self.earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, 
                                Constants.WGS84_EARTH_FLATTENING, 
                                self.ITRF)
        self.inertialFrame = FramesFactory.getEME2000()
    def setup_gsc(self):
        # Sets up ground station (Using GSC2)
        latitude  = radians(1.29761) # degrees
        longitude = radians(103.78036) # degrees
        altitude  = 77.0 # metres
        station = GeodeticPoint(latitude, longitude, altitude)
        self.station_frame = TopocentricFrame(self.earth, station, "Esrange")
        return
    def setup_datetime(self):
        # Sets up start and end date time
        datetime_obj = datetime.strptime(input("Propagation Start Date Time in YYYY/MM/DD HH:MM:SS: "), '%Y/%m/%d %H:%M:%S')
        year, month, day = datetime_obj.year, datetime_obj.month, datetime_obj.day
        hour, minute, second = datetime_obj.hour, datetime_obj.minute, float(datetime_obj.second)
        self.extrapDate = AbsoluteDate(year, month, day, hour, minute, second, TimeScalesFactory.getUTC())
        num_days = int(input("How many days to propagate forward by: "))
        self.finalDate = self.extrapDate.shiftedBy(60.0*60*24*num_days) # seconds
        self.step_size = float(input("Step Size in seconds: ")) # seconds
        return
    def setup_tle(self):
        tle_reference = tle_verify("Reference")
        self.tle_list = [tle_reference, ]
        num_tle = int(input("Number of TLE to verify: "))
        for num in range(num_tle):
            tle_target = tle_verify("Target")
            self.tle_list.append(tle_target)
        return
    def propagation(self):
        # Propagates TLE and generates values
        print(f"Starting Propagation from start date time {self.extrapDate}")
        while self.extrapDate.compareTo(self.finalDate) <= 0.0:
            # Cycles through TLE
            for tle_obj in self.tle_list:
                # Propagates to set date time and generates PV object
                pv = tle_obj.provider.getPVCoordinates(self.extrapDate, self.inertialFrame)
                # Extracts PV values
                pos_tmp = pv.getPosition()
                tle_obj.pos.append((pos_tmp.getX(),pos_tmp.getY(),pos_tmp.getZ()))            
                # Extracts azimuth and elevation values
                az_tmp = self.station_frame.getAzimuth(pos_tmp,
                                self.inertialFrame,
                                self.extrapDate)*180.0/pi # converts to degrees
                el_tmp = self.station_frame.getElevation(pos_tmp,
                                self.inertialFrame,
                                self.extrapDate)*180.0/pi # converts to degrees
                tle_obj.az_el.append((az_tmp, el_tmp))
            # Pushes date time forward by step_size
            self.extrapDate = self.extrapDate.shiftedBy(self.step_size)
        print(f"Ending Propagation with end date time {self.extrapDate}")
        return
    def plots(self):
        # Cycles through TLE
        for tle_obj in self.tle_list:
            # Plots for elevation and azimuth values
            plt.plot(tle_obj.az_el)
            plt.ylim(5, 360)
            plt.title(f'Azimuth and Elevation for {tle_obj.tle_type}')
            plt.grid(True)
            plt.show()
        return

# Creates class tle_object:
class tle_verify():
    def __init__(self, tle_type):
        self.tle_type = tle_type
        self.file_loader()
        self.tle_creation()
        self.prop_creation()
        self.gen_val_creation()
    def file_loader(self):
        # Opens file directory to search for input TLE file
        print(f"Files in Directory TLE")
        for file_item in os.listdir("../../../TLE/TeLEOS-1"):
            print(file_item)
        self.input_file_name = input(f"Input {self.tle_type} TLE file name with txt extension: ")
        self.input_file_path = f"../../../TLE/TeLEOS-1/{self.input_file_name}"
        print("Input file path:", self.input_file_path)
        return
    def tle_creation(self):
        # Sets up TLE object
        with open(self.input_file_path, "r") as file:
            next(file)
            file_content = file.read().splitlines()
            tle_line1 = file_content[0]
            tle_line2 = file_content[1]
        self.tle_for_prop = TLE(tle_line1, tle_line2)
        print (self.tle_for_prop)
        print ('Epoch :', self.tle_for_prop.getDate())
        return
    def prop_creation(self):
        # Sets up propagator for TLE
        propagator = TLEPropagator.selectExtrapolator(self.tle_for_prop)
        self.provider = PVCoordinatesProvider.cast_(propagator)
        return
    def gen_val_creation(self):
        # Sets up azimuth, elevation and position (EME2000 frame) lists
        self.az_el = []
        self.pos = []
        return

x = verify_tle()