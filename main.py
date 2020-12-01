import zeroconf_files.discovery as dis
import zeroconf_files.announce as ann
import threading as th
import time as tm
from configure_data import MY_IP, MY_PORT, MY_NAME, TYPE_SERVICE
from routes import execute_server_flask


if __name__ == "__main__":
    # Configure Discovery/Announce
    discovery = dis.ConfigureDiscovery(TYPE_SERVICE)
    announce = ann.ConfigureAnnounce(ip=MY_IP, port=MY_PORT, name=MY_NAME, name_service=TYPE_SERVICE)

    # Start Discovery/Announce
    discovery.start()
    announce.register_service()

    tm.sleep(3)

    # Start Server Flask in Thread
    app_run_thread = th.Thread(target=execute_server_flask)
    app_run_thread.start()

    tm.sleep(3)

    input("\n\nPress Enter to exit.\n\n")

    # Close Discovery/Announce
    discovery.close()
    announce.unregister_service()
