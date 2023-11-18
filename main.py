import datetime
from enum import Enum, auto
import hashlib
import json
import os
import platform
import shutil
from typing import NamedTuple, Optional

import requests
from robot.api import logger

from tools import get_hash
from zip import extended_ZipFile


class State(Enum):
    INITIAL = auto()
    CHANNEL = auto()
    UPDATE = auto()
    REPAIR = auto()
    LATEST = auto()

class Setup(NamedTuple):
    platform: str
    channel: str
    path: str
    config_path: str

class Config(NamedTuple):
    version: Optional[str] = None
    timestamp: Optional[str] = None
    md5: Optional[str] = None
    state: State = State.UPDATE

class Chrome(NamedTuple):
    path: str
    driver_path: str


def init_setup(channel: str, path: Optional[str]) -> Setup:   # Improve: channel + headless + path

    def process_platform() -> str: # Improve: platforms: linux64, mac-arm64, mac-x64, win32, win64
        supported_platforms = {"Windows": "win64", "Darwin": "mac-arm64", "Linux": "linux64"}
        return supported_platforms.get(platform.system(), "")

    def process_channel(channel: str) -> str: # Improve: channel validation
        return channel.lower().capitalize()

    def process_path(path: Optional[str]) -> str:
        if path is None: return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        elif os.path.exists(path): return path
        else: return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

    def process_config_path(path: str) -> str:
        return os.path.join(path, "cft_config.json")

    path = process_path(path)

    return Setup(
    platform=process_platform(),
    channel=process_channel(channel), 
    path=process_path(path), 
    config_path=process_config_path(path)
    )


def init_config(setup: Setup) -> Config:

    def detect_config(config_path: str) -> bool:
        return os.path.isfile(config_path)

    def process_config(config_path: str) -> dict:
        with open(config_path, "r") as config_file:
            try:
                return json.load(config_file)

            except json.JSONDecodeError: 
                shutil.rmtree(config_path)
                return {}

    def parse_config(config_json: dict) -> Config:
        channel_dict = config_json[setup.platform].get(setup.channel, {})
        md5 = channel_dict.get("last_md5")
        if channel_dict:
            return Config(
                version=channel_dict.get("last_version"),
                timestamp=channel_dict.get("last_update"), 
                md5=md5, 
                state=State.UPDATE if get_hash(os.path.join(setup.path, setup.channel.lower())) == md5 else State.REPAIR
                )

        else:
            return Config(
                state=State.CHANNEL
                )

    if detect_config(Setup.config_path):
        config_json = process_config(setup.config_path)
        return parse_config(config_json)

    else:
        return Config(
            state=State.INITIAL
        )


def init_chromefortesting(config: Config) -> Chrome:

    def check_updates(channel: str, version: str) -> Config:
        if response.status_code == 200:
            remote_version = response.json()["channels"][setup.channel]["version"].replace(".","")
            return Config(
                state=State.UPDATE if remote_version != config.version else State.LATEST
                )

        else:
            return Config(
                state=State.LATEST
                )

    return Chrome




chromelabs_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

def request_chromelabs(url):
    response = requests.get(chromelabs_endpoint_url)

def fetch_binaries() -> bytes
#     chrome_source = response.json()["channels"][channel]["downloads"]["chrome"]
#     chromedriver_source = response.json()["channels"][channel]["downloads"]["chromedriver"]

    chrome_source = requests.get(chrome["url"])
    chromedriver_source = requests.get(chromedriver["url"])






# def download(channel, output_bin, request) -> None:
#     chrome_source = response.json()["channels"][channel]["downloads"]["chrome"]
#     chromedriver_source = response.json()["channels"][channel]["downloads"]["chromedriver"]

#     for chrome, chromedriver in zip(chrome_source, chromedriver_source):    # TBD: Progress bars
#         if platform == chrome["platform"] == chromedriver["platform"]:
#             channel_dir = os.path.join(output_bin, channel.lower())

#             if os.path.exists(channel_dir): shutil.rmtree(channel_dir)
#             os.makedirs(channel_dir, exist_ok=True)
#             [os.remove(os.path.join(output_bin, file)) for file in os.listdir(output_bin) if file.endswith('.zip')]

#             chrome_source = requests.get(chrome["url"])
#             chromedriver_source = requests.get(chromedriver["url"])
#             chrome_zip = os.path.join(output_bin, f"chrome_{current_version}.zip")
#             chromedriver_zip = os.path.join(output_bin, f"chromedriver_{current_version}.zip")

#             with open(chrome_zip, "wb") as file:
#                 file.write(chrome_source.content)

#             with extended_ZipFile(chrome_zip, "r") as archive:
#                 archive.extractall(channel_dir)
#             os.remove(chrome_zip)

#             with open(chromedriver_zip, "wb") as file:
#                 file.write(chromedriver_source.content)

#             with extended_ZipFile(chromedriver_zip, "r") as archive:
#                 archive.extractall(channel_dir)
#             os.remove(chromedriver_zip)
#             break



#     def write_config(config_path, platform, channel, version, timestamp, md5) -> None:
#         if os.path.isfile(config_path):
#             with open(config_path, "r") as json_file:
#                 config_data = json.load(json_file)

#             if platform in config_data and channel in config_data[platform]:
#                 config_data[platform][channel].update({
#                                                     "last_version": version,
#                                                     "last_update": timestamp,
#                                                     "last_md5": md5
#                                                 })

#             else:
#                 config_data[platform][channel] = {
#                     "last_version": version,
#                     "last_update": timestamp,
#                     "last_md5": md5
#                 }

#             with open(config_path, "w") as json_file:
#                     json.dump(config_data, json_file, indent=4)

#         else:
#             with open(config_path, "w") as json_file:
#                     json.dump({
#                         platform: {
#                             channel: {
#                                 "last_version": version,
#                                 "last_update": timestamp,
#                                 "last_md5": md5
#                             }
#                         }
#                     }, json_file, indent=4)


#     def expose_binaries(chrome: Chrome) -> str:
#         for path in paths:
#             os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])   # TBD: Experiment with path ordering
        # return

#     if state: 
#         write_config(config_path, platform, channel, current_version, str(datetime.datetime.now(datetime.timezone.utc)), generate_md5(os.path.join(output_bin, channel.lower())))
#         expose_binaries(paths)
#     else:
#         # Log: Fail
#         pass


# Process output_path with backslash escape on Windows