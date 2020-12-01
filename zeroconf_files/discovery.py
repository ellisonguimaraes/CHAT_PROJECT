from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
from socket import inet_ntoa
from repository.repository import UserRepository
from models.user import User


class Listener(ServiceListener):
    def update_service(self, zc: 'zeroconf_files', type_: str, name: str) -> None:
        # Getter Service Info (ZeroConf)
        info_service = zc.get_service_info(type_, name)

        print("Um serviço foi ATUALIZADO:")
        self.print_info_service(info_service)

        # Getter user with name
        user = UserRepository.get_by_name(name)

        # Data Update
        user.ip = str(inet_ntoa(info_service.addresses[0]))
        user.port = str(info_service.port)

        # Database Update
        UserRepository.update(user)

    def remove_service(self, zc: 'zeroconf_files', type_: str, name: str):
        print(f'Um serviço foi removido: Tipo: {type_} Nome: {name}')

        # Getter user with name
        user = UserRepository.get_by_name(name)

        # Update Status (0 = OFF, 1 = ON)
        user.status = 0

        # Database Update
        UserRepository.update(user)

    def add_service(self, zc: 'zeroconf_files', type_: str, name: str):
        info_service = zc.get_service_info(type_, name)
        print("Um serviço foi ENCONTRADO:")
        self.print_info_service(info_service)

        # Getter user with name
        user = UserRepository.get_by_name(name)

        # If user is equal None, user not exists
        if user is None:
            # Created User
            UserRepository.save(User(None, str(info_service.name), str(inet_ntoa(info_service.addresses[0])), str(info_service.port), 1))
        else:
            # Update Status Code
            user.status = 1
            UserRepository.update(user)

    @staticmethod
    def print_info_service(info_service):
        print(f"Tipo: {info_service.type}\n"
              f"Name: {info_service.name}\n"
              f"IP: {str(inet_ntoa(info_service.addresses[0]))}:{info_service.port}\n"
              f"*********************************\n")


class ConfigureDiscovery:
    def __init__(self, name_service):
        self.zeroconf = Zeroconf()
        self.listener = Listener()
        self.name_service = name_service
        self.service_browser = None

    def start(self):
        # Start to Listener Discovery
        self.service_browser = ServiceBrowser(self.zeroconf, self.name_service, self.listener)

    def close(self):
        # Close to Listener Discovery
        self.zeroconf.close()


