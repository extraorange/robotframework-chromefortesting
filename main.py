#!/usr/bin/env python

"""
robotframework-chromefortesting
Chrome for Testing (CfT) for Robot Framework

├── robotframework-chromefortesting.py    +
├── ${output_bin}                         +
│ ├── [platform]/                         +
│ │ ├── chrome-[platform]/                +
│ │ └── chromedriver-[platform]           +
│ └── chromefortesting_config.json        +

GitHub: https://github.com/extraorange/robotframework-chromefortesting

Disclaimer: Distributed as-is, without warranties or guarantees.

Author: d***X
Date: 13 Nov 2023
Version: 0.4 (pre-release)
License: GNU General Public License v3.0

"""

import datetime
import hashlib
import json
import logging
import os
import platform as read_platform
import shutil
from typing import Tuple
from zipfile import ZipFile, ZipInfo

import requests
from robot.api import logger
from robot.api.deco import keyword

chromelabs_endpoint_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

class extended_ZipFile(ZipFile): # Safeguard permissions translation across platforms.
    def _extract_member(self, member, path, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)
        path = super()._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        if attr != 0: os.chmod(path, attr)
        return path

def generate_md5(output_bin, algorithm="md5", block_size=65536) -> str:

    def calculate_checksum(file_path, algorithm, block_size) -> str:
        hash_function = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            block = file.read(block_size)
            while len(block) > 0:
                hash_function.update(block)
                block = file.read(block_size)
        return hash_function.hexdigest()

    for root, dirs, files in os.walk(output_bin):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            checksum = calculate_checksum(file_path, algorithm, block_size)
            ([]).append(checksum)
    md5 = "".join([])
    return md5

def write_config(config_path, platform, channel, version, timestamp, md5) -> None:
    if os.path.isfile(config_path):
        with open(config_path, "r") as json_file:
            config_data = json.load(json_file)

        if f"{platform}" in config_data and f"{channel}" in config_data[f"{platform}"]:
            config_data[f"{platform}"][f"{channel}"]["last_version"] = version
            config_data[f"{platform}"][f"{channel}"]["last_update"] = timestamp
            config_data[f"{platform}"][f"{channel}"]["last_md5"] = md5

        else:
            config_data[f"{platform}"] = {
                            f"{channel}": {
                                "last_version": version,
                                "last_update": timestamp,
                                "last_md5": md5
                }
            }

        with open(config_path, "a") as json_file:
            json.dump(config_data, json_file, indent=4)

    else:
        with open(config_path, "w") as json_file:
            json.dump({f"{platform}": {
                            f"{channel}": {
                                "last_version": version,
                                "last_update": timestamp,
                                "last_md5": md5
                                }
                            }
                        }, json_file, indent=4)

def expose_binaries(*paths) -> None: # TBD: Part of exit()
    for path in paths:
        os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])

def init_nodes(channel: str, output_bin: str) -> Tuple[str, str, str, str]:

    def detect_platform() -> str: # TBD: Flexify
        supported_platforms = {
            "Windows": "win64",
            "Darwin": "mac-arm64",
            "Linux": "linux64"
        }
        return supported_platforms.get(read_platform.system(), "")

    channel = channel.lower().capitalize()
    output_bin = output_bin if output_bin is not None and os.path.exists(output_bin) else os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    config_path = os.path.join(output_bin, channel, "chromefortesting_config.json")
    return detect_platform(), channel, output_bin, config_path



@keyword("Initialise Chrome For Testing")
def main(channel: str = "Stable", output_bin: str = ""):

    global initialised, config_error
    platform, channel, output_bin, config_path = init_nodes(channel, output_bin)

    # func initialised() -> bool:
    if os.path.exists(config_path):

        # func read_config() -> ? :
        try:
            with open(config_path, "r") as file:
                config_data = json.load(file)
                if platform in config_data and channel in config_data:
                    last_version = config_data.get(platform, {}).get("last_version")
                    last_update = config_data.get(platform, {}).get("last_update")
                    last_md5 = config_data.get(platform, {}).get("last_md5")
                    initialised = generate_md5(os.path.join(output_bin, platform)) != last_md5

        except json.JSONDecodeError:
            logging.error("Compromised configuration file detected. Rebuilding...")
            os.remove(config_path)
            initialised = False

    else:
        initialised = False

    if not initialised:
        logger.info("CfT: Setup initialisation...")

        # func fetch_updates(platform, channel) -> ? :
        response = requests.get(chromelabs_endpoint_url)
        if response.status_code == 200:
            current_version = response.json()["channels"][channel]["version"]
            initialised = True if os.path.exists(config_path) else (int(current_version.replace(".", "")) > int(last_version.replace(".", ""))) if 'last_version' in locals() else False

            if not initialised:

                # func obtain_binaries() -> (chrome binary, chromedriver binary):
                chrome_source = response.json()["channels"][channel]["downloads"]["chrome"]
                chromedriver_source = response.json()["channels"][channel]["downloads"]["chromedriver"]

                for chrome, chromedriver in zip(chrome_source, chromedriver_source):
                    if platform == chrome["platform"] == chromedriver["platform"]:

                        channel_dir = os.path.join(output_bin, channel.lower())
                        # func update_setup() -> None:
                        if os.path.exists(channel_dir): shutil.rmtree(channel_dir)
                        os.makedirs(channel_dir, exist_ok=True)
                        [os.remove(os.path.join(output_bin, file)) for file in os.listdir(output_bin) if file.endswith('.zip')]

                        chrome_source = requests.get(chrome["url"])
                        chromedriver_source = requests.get(chromedriver["url"])
                        chrome_zip = os.path.join(output_bin, f"chrome_{current_version}.zip")
                        chromedriver_zip = os.path.join(output_bin, f"chromedriver_{current_version}.zip")

                        # func put_binaries(chrome_source, chromedriver_source) -> (str, str):
                        with open(chrome_zip, "wb") as file:
                            file.write(chrome_source.content)

                        with extended_ZipFile(chrome_zip, "r") as archive:
                            archive.extractall(channel_dir)
                        os.remove(chrome_zip)

                        with open(chromedriver_zip, "wb") as file:
                            file.write(chromedriver_source.content)

                        with extended_ZipFile(chromedriver_zip, "r") as archive:
                            archive.extractall(channel_dir)
                        os.remove(chromedriver_zip)
                        break

                    # func exit(2) -> None:
                logger.info(f"CfT: New latest version in use: {current_version}. Initiating Robot Framework automation...")
                write_config(config_path, platform, channel, current_version, str(datetime.datetime.now(datetime.timezone.utc)), generate_md5(output_bin))
                expose_binaries(os.path.join(output_bin, channel, f"chrome-{platform}"), os.path.join(output_bin, channel, f"chrome-{platform}"))

        else:
                # func exit(1) -> None:
            # logger.warning("Update status check unsuccessful. Connectivity issues detected. Initiating Robot Framework automation...")
            expose_binaries(os.path.join(output_bin, channel, f"chrome-{platform}"), os.path.join(output_bin, channel, f"chrome-{platform}"))

    else:
        # func exit(0) -> None:
        logger.info("CfT: Initiating Robot Framework automation...")
        expose_binaries(os.path.join(output_bin, channel, f"chrome-{platform}"), os.path.join(output_bin, channel, f"chrome-{platform}"))

if __name__ == "__main__":
    main()