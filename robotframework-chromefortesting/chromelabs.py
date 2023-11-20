import os
from typing import Optional

import requests
from requests.models import Response

from state import State
from toolkit import get_hash, get_timestap, process_extract_assets, reset_assets_location


class ChromeAssets():
    def __init__(self, chrome_path: str, chromedriver: str, version: Optional[str] = None, timestamp: Optional[str] = None, md5: Optional[str] = None, headless: bool = False) -> None:
        self.chrome: str = chrome_path
        self.chromedriver: str = chromedriver
        self.version: Optional[str] = version
        self.timestamp: Optional[str] = timestamp
        self.md5: Optional[str] = md5
        self.headless: bool = headless

    def expose_to_system(self) -> None:
        for path in [self.chrome, self.chromedriver]:
            os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])

    def return_chrome_binary_path(self) -> str:
        #! Windows path processing for Robot Framework
        return self.chrome


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

def get_current_version(channel: str) -> str:
    response = request_chromelabs()
    return response.json()["channels"][channel]["version"] if response else ""

def load_assets(config) -> ChromeAssets:

    if config.state is not State.LATEST:
        response = request_chromelabs()
        if response and config.state != State.LATEST:
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

            chrome_path = os.path.join(config.channel_path, f"chrome-{config.platform}") if not config.headless else os.path.join(config.channel_path, f"chrome-headless-shell-{config.platform}")
            chromedriver_path = os.path.join(config.channel_path, f"chromedriver-{config.platform}")
            return ChromeAssets(
                chrome_path, 
                chromedriver_path, 
                get_current_version(config.channel), 
                get_timestap(), 
                get_hash(config.channel_path), 
                config.headless
                )
                
        else: 
            return ChromeAssets("", "")

    else:
        chrome_path = os.path.join(config.channel_path, f"chrome-{config.platform}") if not config.headless else os.path.join(config.channel_path, f"chrome-headless-shell-{config.platform}")
        chromedriver_path = os.path.join(config.channel_path, f"chromedriver-{config.platform}")
        return ChromeAssets(
            chrome_path, 
            chromedriver_path
            )