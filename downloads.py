from typing import NamedTuple, Optional

import requests
from requests.models import Response


chromelabs_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"


class ChromeAssets(NamedTuple):
    path: str
    driver_path: str


def get_chromelabs_data(url: str) -> Optional[Response]:
    response = requests.get(url)
    return response if response.status_code == 200 else None

def check_updates(channel: str, current_version: str) -> bool:
    response = get_chromelabs_data(chromelabs_url)
    remote_version = response.json()["channels"][channel]["version"] if response else None
    return False if current_version == remote_version else False