from dataclasses import dataclass


@dataclass
class ServiceInfoProvider:
    info: 'Service' = None

    @property
    def service(self):
        return self.info

    @service.setter
    def service(self, value: 'Service'):
        self.info = value


info_provider = ServiceInfoProvider()


def get_service_info() -> 'Service':
    return info_provider.service


def set_service_info(info: 'Service') -> None:
    info_provider.service = info
