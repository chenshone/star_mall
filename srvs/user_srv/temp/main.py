# import requests

# headers = {
#     "contentType": "application/json",
# }

# def register(name, id, address, port):
#     url = "http://127.0.0.1:8500/v1/agent/service/register"
#     resp = requests.put(url, headers=headers, json={
#         "Name": name,
#         "ID": id,
#         "Tags": ["star_mall", "srv"],
#         "Address": address,
#         "Port": port,
#         "Check": {
#             "GRPC": f"{address}:{port}",
#             "GRPCUseTLS": False,
#             "Timeout": "5s",
#             "Interval": "5s",
#             "DeregisterCriticalServiceAfter": "5s"
#         }
#     })

#     if resp.status_code == 200:
#         print("register success")
#     else:
#         print("register failed")


# def deregister(id):
#     url = f"http://127.0.0.1:8500/v1/agent/service/deregister/{id}"
#     resp = requests.put(url, headers=headers)
#     if resp.status_code == 200:
#         print("deregister success")
#     else:
#         print("deregister failed")


import consul
import requests

c = consul.Consul(host="127.0.0.1", port=8500)

address="192.168.10.5"
port = 50051
check = {"GRPC": f"{address}:{port}","GRPCUseTLS": False,"Timeout": "5s","Interval": "5s","DeregisterCriticalServiceAfter": "15s"
}

resp = c.agent.service.register(name="star_mall-srv", service_id="star_mall-srv", address=address, port=port, tags=["star_mall", "srv"],check=check)

print(resp)

def fill_service(name):
    url = "http://127.0.0.1:8500/v1/agent/services"
    params = {
        "filter": f"Service == {name}"
    }
    resp = requests.get(url, params=params).json()
    for key, value in resp.items():
        print(key)

# if __name__ == '__main__':
#     register("star_mall-srv", "star_mall-srv", "192.168.10.5", 50051)
#     # deregister("star_mall-srv")
