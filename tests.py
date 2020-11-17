import requests
import json
from tzlocal import get_localzone #pip install tzlocal

url = "http://localhost:8000/"
local_tz_name = get_localzone().__str__()

print(requests.get(url))

print(requests.get(url + "UTC"))

print(requests.get(url + "Europe/Moscow"))

print(requests.get(url + "api/v1/time"))

print(requests.get(url + "api/v1/date"))

print(requests.get(url + "api/v1/time", params={"tz": "UTC"}))

print(requests.get(url + "api/v1/time", params={"tz": "Europe/Moscow"}))

print(requests.get(url + "api/v1/date", params={"tz": "Europe/Moscow"}))

print(requests.post(url + "api/v1/datediff", data= json.dumps({
    "start": {
        "date": "12:30pm 2020-12-01"
    },
    "end": {
        "date": "12.20.2021 22:21:05",
        "tz": "UTC"
    }
})))

print(requests.post(url + "api/v1/datediff", data= json.dumps({
    "start": {
        "date": "12:30pm 2020-12-01"
    },
    "end": {
        "date": "12.24.2021 22:21:05",
        "tz": "UTC"
    }
})))