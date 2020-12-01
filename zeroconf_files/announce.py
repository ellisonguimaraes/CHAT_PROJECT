from socket import inet_aton, inet_ntoa
from zeroconf import Zeroconf, ServiceInfo


class ConfigureAnnounce:
    def __init__(self, ip, port, name, name_service):
        self.service_info = ServiceInfo(
            type_=name_service,
            name=name + "." + name_service,
            port=port,
            addresses=[inet_aton(ip)]
        )
        self.zeroconf = Zeroconf()

    def register_service(self):
        self.zeroconf.register_service(self.service_info)
        print(f'Serviço Anunciado: {str(inet_ntoa(self.service_info.addresses[0]))}:{self.service_info.port}\n')

    def unregister_service(self):
        self.zeroconf.unregister_service(self.service_info)
        print(f'Serviço Removido: {str(inet_ntoa(self.service_info.addresses[0]))}:{self.service_info.port}\n')

