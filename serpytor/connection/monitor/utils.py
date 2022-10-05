import requests


def detect_ip() -> str:
    req = requests.get("https://api.ipify.org/?format=json").json()
    return req["ip"]
