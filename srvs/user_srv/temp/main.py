import requests

headers = {
    "contentType": "application/json",
}


def register(name, id, address, port):
    url = "http://127.0.0.1:8500/v1/agent/service/register"
    resp = requests.put(
        url,
        headers=headers,
        json={
            "Name": name,
            "ID": id,
            "Tags": ["star_mall", "srv"],
            "Address": address,
            "Port": port,
            "Check": {
                # "HTTP": f"http://{address}:{port}/health",
                "GRPC": f"{address}:{port}",
                "GRPCUseTLS": False,
                "Timeout": "5s",
                "Interval": "5s",
                "DeregisterCriticalServiceAfter": "5s",
            },
        },
    )

    if resp.status_code == 200:
        print("register success")
    else:
        print("register failed")


def deregister(id):
    url = f"http://127.0.0.1:8500/v1/agent/service/deregister/{id}"
    resp = requests.put(url, headers=headers)
    if resp.status_code == 200:
        print("deregister success")
    else:
        print("deregister failed")


def fill_service(name):
    url = "http://127.0.0.1:8500/v1/agent/services"
    params = {"filter": f'Service == "{name}"'}
    resp = requests.get(url, params=params).json()
    for key, value in resp.items():
        print(key)
        print(value)


if __name__ == "__main__":
    # register("user-srv", "user-srv", "127.0.0.1", 50051)
    # fill_service("user-srv")
    deregister("user-web")
