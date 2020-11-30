import Zeroconf.Discovery as des
import Zeroconf.Announce as anu
from configure_data import *
import sys


if __name__ == '__main__':

    # Configure Discovery/Announce
    discovery = des.ConfigureDiscovery(TYPE_SERVICE)
    announce = anu.ConfigureAnnounce(ip=MY_IP, port=MY_PORT, name=MY_NAME, name_service=TYPE_SERVICE)

    # Start Discovery/Announce
    discovery.start()
    announce.register_service()

    input("\n\nPress Enter to exit.\n\n")

    # Close Discovery/Announce
    discovery.close()
    announce.unregister_service()