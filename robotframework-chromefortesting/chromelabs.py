import os
from typing import Optional

import requests
from requests.models import Response

from config import Config
from toolkit import get_hash, get_timestap, process_extract_assets, reset_assets_location


def request_chromelabs() -> Optional[Response]:
    response = requests.get("https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json")
    return response if response.status_code == 200 else None

def check_updates(channel: str, version: str) -> bool:
    response = request_chromelabs()
    if response:
        remote_version = response.json()["channels"][channel]["version"]
        return version != remote_version
    else: 
        return False

def load_assets(config: Config) -> ChromeAssets:

    def get_current_version(channel: str) -> str:
        response = request_chromelabs()
        return response.json()["channels"][channel]["version"] if response else ""

    response = request_chromelabs()
    if response:
        if config.headless: chrome_pool = response.json()["channels"][config.channel]["downloads"]["chrome-headless-shell"]
        else: chrome_pool = response.json()["channels"][config.channel]["downloads"]["chrome"]
        chromedriver_pool = response.json()["channels"][config.channel]["downloads"]["chromedriver"]

        for _chrome, _chromedriver in zip(chrome_pool, chromedriver_pool):
            if config.platform == _chrome["platform"] == _chromedriver["platform"]:

                reset_assets_location(config.channel_path)
                _chromezip_bytes = requests.get(_chrome["url"])
                _chromedriver_zip_bytes = requests.get(_chromedriver["url"])
                version = get_current_version(config.channel)
                process_extract_assets(version, config.channel_path, _chromezip_bytes, _chromedriver_zip_bytes)
                break
        
        chrome_path = os.path.join(config.channel_path, f"chrome-{config.platform}") if not config.headless else os.path.join(config.channel_path, f"chrome-headless-shell{config.platform}")
        chromedriver_path = os.path.join(config.channel_path, f"chromedriver-{config.platform}")
        return ChromeAssets(chrome_path, chromedriver_path, get_current_version(config.channel), get_timestap(), get_hash(config.channel_path))

    else:
        chrome_path = os.path.join(config.channel_path, f"chrome-{config.platform}") if not config.headless else os.path.join(config.channel_path, f"chrome-headless-shell{config.platform}")
        chromedriver_path = os.path.join(config.channel_path, f"chromedriver-{config.platform}")
        return ChromeAssets(chrome_path, chromedriver_path)