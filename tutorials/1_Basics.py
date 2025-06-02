import orekit
vm = orekit.initVM()
print('Java version:',vm.java_version)
print('Orekit version:', orekit.VERSION)

from orekit.pyhelpers import setup_orekit_curdir, download_orekit_data_curdir
setup_orekit_curdir(from_pip_library=True)

from org.orekit.utils import Constants
print(Constants.WGS84_EARTH_EQUATORIAL_RADIUS)