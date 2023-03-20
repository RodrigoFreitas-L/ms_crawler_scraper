import requests
from time import sleep


def fetch(url):
    try:
        sleep(2)
        header = {"user-agent": "Fake user-agent"}
        response = requests.get(url, headers=header, timeout=5)
    except requests.ReadTimeout:
        return None
    if response.status_code == 200:
        return response.text
    return None
