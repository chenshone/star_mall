import requests
from common.register import base
import consul


class ConsulRegister(base.Register):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.c = consul.Consul(host=host, port=port)

    def register(self, name, service_id, address, port, tags, check=None) -> bool:
        if check is None:
            check = {
                "GRPC": f"{address}:{port}",
                "GRPCUseTLS": False,
                "Timeout": "5s",
                "Interval": "5s",
                "DeregisterCriticalServiceAfter": "15s",
            }
        else:
            check = check

        ok = self.c.agent.service.register(
            name=name,
            service_id=service_id,
            address=address,
            port=port,
            tags=tags,
            check=check,
        )

        if ok:
            return True
        return False

    def deregister(self, service_id):
        return self.c.agent.service.deregister(service_id)

    def get_all_services(self):
        return self.c.agent.services()

    def filter_services(self, filter):
        url = f"http://{self.host}:{self.port}/v1/agent/services"
        params = {
            "filter": filter,
        }
        resp = requests.get(url=url, params=params)
