import Zeroconf.Discovery as des
import Zeroconf.Announce as anu
from Repository.Repository import UserRepository
from Models.User import User

# ZeroConf Data Configure (Discovery/Announce ZeroConf)
TYPE_SERVICE = "_sd-chat-host._tcp.local."
MY_IP = "192.168.1.101"
MY_PORT = 5555
MY_NAME = "ellison"


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
