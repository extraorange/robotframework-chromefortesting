#!/usr/bin/env python
import datetime
from enum import Flag
import hashlib
import json
import os
import platform as read_platform
import shutil
from sys import platform
from typing import NamedTuple, Union

import requests
from robot.api import logger

from zip import extended_ZipFile

chromelabs_endpoint_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

class SetupData(NamedTuple):
    platform: str
    channel: str
    path: str
    config_path: str

class ConfigData(NamedTuple):
    version: Union[str, None]
    timestamp: Union[str, None]
    md5: Union[str, None]

class _MainStatus(NamedTuple):
    initial: int = 1
    channel: int = 0
    repair: int = -1

class _ExitStatus(NamedTuple):
    updated: int = 2
    latest: int = 0
    failed: int = -1

def get_setup(channel: str, path: Union[None, str]) -> SetupData:

    def process_platform() -> str:
        supported_platforms = {
            "Windows": "win64",
            "Darwin": "mac-arm64",
            "Linux": "linux64"
        }
        return supported_platforms.get(read_platform.system(), "")

    def process_channel(channel: str) -> str:
        return channel.lower().capitalize()

    def process_path(path: Union[None, str]) -> str:
        if path is None: return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        elif os.path.exists(path): return path
        else: return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

    def process_config_path(path: str) -> str:
        return os.path.join(path, "cft_config.json")

    path = process_path(path)

    return SetupData(platform=process_platform(),
                     channel=process_channel(channel),
                     path=process_path(path),
                     config_path=process_config_path(path))


def read_config(setup_data: SetupData) -> Union[ConfigData, int]:

    if os.path.isfile(setup_data.config_path):
        with open(setup_data.config_path, "r") as config_file:
            config_data_json = json.load(config_file)

        if setup_data.platform and setup_data.channel in config_data_json :
            try:
                return ConfigData(
                    version=config_data_json[setup_data.platform].get(setup_data.channel).get("last_version"),
                    timestamp=config_data_json[setup_data.platform].get(setup_data.channel).get("last_update"),
                    md5=config_data_json[setup_data.platform].get(setup_data.channel).get("last_md5")
                                )

            except Exception as e:
                logger.error(f"{e}: Compromised configuration file detected.")    # Log error
                shutil.rmtree(setup_data.config_path)
                return _MainStatus.repair

        else:
            return _MainStatus.channel

    return _MainStatus.initial


def assess_init(setup_data: SetupData, config_data: ConfigData) -> bool:

    if ConfigData:
        return get_hash(os.path.join(setup_data.path, setup_data.channel.lower())) == config_data.md5

    elif _MainStatus.initial:
        pass # Log info: Initialising setup
    elif _MainStatus.channel: 
        pass # Log info: Initialising new channel setup
    else _MainStatus.repair:
        pass # Log info: Reinitializing Chrome for Testing setup


def get_hash(path: str) -> str:

    def calc_hash(path: str) -> str:
        hash_func = hashlib.new("md5")
        with open(path, 'rb') as file:
            block = file.read(4096)
            while len(block) > 0:
                hash_func.update(block)
                block = file.read(4096)
        return hash_func.hexdigest()

    return "".join([calc_hash(os.path.join(root, file)) for root, _, files in os.walk(path) for file in files])


# def download(channel, output_bin) -> None:
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


# def exit(status: int, *paths) -> str:
#     # status = 2 : update
#     # status = 1 : initial setup / latest update
#     # status = 0 : no response / no connection

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

#     def expose_binaries(paths) -> None:
#         for path in paths:
#             os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])   # TBD: Experiment with path ordering

#     if status: 
#         write_config(config_path, platform, channel, current_version, str(datetime.datetime.now(datetime.timezone.utc)), generate_md5(os.path.join(output_bin, channel.lower())))
#         expose_binaries(paths)
#     else:
#         # Log: Fail
#         pass