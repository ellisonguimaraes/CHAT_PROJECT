import sys

# ZeroConf Data Configure (Discovery/Announce ZeroConf)
TYPE_SERVICE = "_sd-chat-host._tcp.local."
MY_IP = sys.argv[1]
MY_PORT = int(sys.argv[2])
MY_NAME = sys.argv[3]