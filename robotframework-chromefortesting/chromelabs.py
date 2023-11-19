import os
from typing import NamedTuple, Optional

import requests
from requests.models import Response

from toolkit import PureUnzip


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


###############################################
def fetch_binaries() -> bytes:
    chrome_collection = response.json()["channels"][channel]["downloads"]["chrome"]
    chromedriver_collection = response.json()["channels"][channel]["downloads"]["chromedriver"]

    for chrome, chromedriver in zip(chrome_source, chromedriver_source):
        if platform == chrome["platform"] == chromedriver["platform"]:

def install_chromefortesting(channel, output_bin, request) -> None:

    chrome = response.json()["channels"][channel]["downloads"]["chrome"]
    chromedriver_source = response.json()["channels"][channel]["downloads"]["chromedriver"]

    
    channel_dir = os.path.join(output_bin, channel.lower())

    if os.path.exists(channel_dir): shutil.rmtree(channel_dir)
    os.makedirs(channel_dir, exist_ok=True)
    [os.remove(os.path.join(output_bin, file)) for file in os.listdir(output_bin) if file.endswith('.zip')]

    chrome_source = requests.get(chrome["url"])
    chromedriver_source = requests.get(chromedriver["url"])
    chrome_zip = os.path.join(output_bin, f"chrome_{current_version}.zip")
    chromedriver_zip = os.path.join(output_bin, f"chromedriver_{current_version}.zip")

    with open(chrome_zip, "wb") as file:
        file.write(chrome_source.content)

    with PureUnzip(chrome_zip, "r") as archive:
        archive.extractall(channel_dir)
    os.remove(chrome_zip)

    with open(chromedriver_zip, "wb") as file:
        file.write(chromedriver_source.content)

    with PureUnzip(chromedriver_zip, "r") as archive:
        archive.extractall(channel_dir)
    os.remove(chromedriver_zip)
    break