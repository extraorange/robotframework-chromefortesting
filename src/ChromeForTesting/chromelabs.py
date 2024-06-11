import os
import shutil
from typing import Optional, Tuple

import requests
from requests.models import Response

from .toolkit import ExtendedZipFile, get_hash, get_timestap, set_permissions

class ChromeAssets():
    def __init__(self, chrome_path: str, chromedriver: str, version: Optional[str] = None, timestamp: Optional[str] = None, md5: Optional[str] = None, headless: bool = False):
        self.chrome: str = chrome_path
        self.chromedriver: str = chromedriver
        self.version: Optional[str] = version
        self.timestamp: Optional[str] = timestamp
        self.md5: Optional[str] = md5
        self.headless: bool = headless

    def expose_to_system(self):
        for path in [self.chrome, self.chromedriver]:
            os.environ['PATH'] = os.path.abspath(path) + os.pathsep + os.environ.get('PATH', '')

def request_chromelabs() -> Response | None:
    response = requests.get("https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json")
    return response if response.status_code == 200 else None

def get_current_version(channel: str) -> str:
    response = request_chromelabs()
    return response.json()["channels"][channel]["version"] if response else ""

def check_updates(channel: str, version: str) -> bool:
    response = request_chromelabs()
    if response:
        remote_version = response.json()["channels"][channel]["version"]
        return version != remote_version
    else: 
        return False

def detect_local_assets(config) -> bool:
    chrome_path = os.path.join(config.channel_path, f"chrome-{config.platform}") if not config.headless else os.path.join(config.channel_path, f"chrome-headless-shell-{config.platform}")
    chromedriver_path = os.path.join(config.channel_path, f"chromedriver-{config.platform}")
    if os.path.isdir(chrome_path) and os.path.isdir(chromedriver_path):
        return True
    else:
        reset_local_assets(config.channel_path)
        return False

def reset_local_assets(path: str) -> None:
    if os.path.exists(path): 
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    [os.remove(os.path.join(path, file)) for file in os.listdir(path) if file.endswith('.zip')]

def fetch_assets_zip(response: Response, config) -> Tuple[Response, Response] | None:
    if config.headless: chrome_pool = response.json()["channels"][config.channel]["downloads"]["chrome-headless-shell"]
    else: chrome_pool = response.json()["channels"][config.channel]["downloads"]["chrome"]
    chromedriver_pool = response.json()["channels"][config.channel]["downloads"]["chromedriver"]
    for _chrome, _chromedriver in zip(chrome_pool, chromedriver_pool):
        if config.platform == _chrome["platform"] == _chromedriver["platform"]:
            reset_local_assets(config.channel_path)
            chromezip_bytes = requests.get(_chrome["url"])
            chromedriver_zip_bytes = requests.get(_chromedriver["url"])
            return chromezip_bytes, chromedriver_zip_bytes

def extract_assets(version: str, config, *_bytes: Response) -> Tuple[str, str]:
    zip_path = os.path.join(config.channel_path, f"chrome_{version}.zip")
    for bytes in _bytes:
        with open(zip_path, "wb") as file:
            file.write(bytes.content)
        with ExtendedZipFile(zip_path, "r") as archive:
            archive.extractall(config.channel_path)
        os.remove(zip_path)
    chrome_path = os.path.join(config.channel_path, f"chrome-{config.platform}") if not config.headless else os.path.join(config.channel_path, f"chrome-headless-shell-{config.platform}")
    chromedriver_path = os.path.join(config.channel_path, f"chromedriver-{config.platform}")
    return chrome_path, chromedriver_path

def download_assets(config) -> ChromeAssets:
    response = request_chromelabs()
    if response:
        version = get_current_version(config.channel)
        download_result = fetch_assets_zip(response, config)
        if download_result:
            chromezip_bytes, chromedriver_zip_bytes = download_result
            chrome_path, chromedriver_path = extract_assets(version, config, chromezip_bytes, chromedriver_zip_bytes)
            if detect_local_assets(config):
                set_permissions(config.platform, chrome_path, chromedriver_path)
                return ChromeAssets(
                    chrome_path, 
                    chromedriver_path, 
                    version, 
                    get_timestap(), 
                    get_hash(config.channel_path), 
                    config.headless
                    )

def update_assets(config) -> ChromeAssets:
    response = request_chromelabs()
    if response:
        version = get_current_version(config.channel)
        download_result = fetch_assets_zip(response, config)
        if download_result:
            chromezip_bytes, chromedriver_zip_bytes = download_result
            reset_local_assets(config.channel_path)
            chrome_path, chromedriver_path = extract_assets(version, config, chromezip_bytes, chromedriver_zip_bytes)
            if detect_local_assets(config):
                set_permissions(config.platform, chrome_path, chromedriver_path)
                return ChromeAssets(
                    chrome_path, 
                    chromedriver_path, 
                    get_current_version(config.channel), 
                    get_timestap(), 
                    get_hash(config.channel_path), 
                    config.headless
                    )

def load_local_assets(config) -> ChromeAssets:
    detect_local_assets(config)
    chrome_path = os.path.join(config.channel_path, f"chrome-{config.platform}") if not config.headless else os.path.join(config.channel_path, f"chrome-headless-shell-{config.platform}")
    chromedriver_path = os.path.join(config.channel_path, f"chromedriver-{config.platform}")
    set_permissions(config.platform, chrome_path, chromedriver_path)
    return ChromeAssets(
        chrome_path, 
        chromedriver_path
    )
