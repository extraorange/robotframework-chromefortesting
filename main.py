#!/usr/bin/env python

"""
robotframework-chromefortesting
Chrome for Testing (CfT) for Robot Framework

├── ${bin_path}                   +
│   ├── [platform]/               +
│   │   ├── chromedriver          +
│   │   └── chrome_[platform]/    +
│   └── cft_config.json           +

GitHub: https://github.com/dunexplorer/robotframework-chromefortesting

Disclaimer: Distributed as-is, without warranties or guarantees.

Author: dX
Date: 13 Nov 2023
Version: 0.3
License: GNU General Public License v3.0
p
"""

import datetime
import hashlib
import json
import logging
import os
import platform
import requests
import shutil
from zipfile import ZipFile, ZipInfo

from robot.api import logger
from robot.api.deco import keyword

chromelabs_endpoint_url = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

class extended_ZipFile(ZipFile): # Extending to safeguard permissions translation across platforms.
    def _extract_member(self, member, path, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)
        path = super()._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        if attr != 0: os.chmod(path, attr)
        return path

def generate_md5(binary_path, algorithm="md5", block_size=65536) -> str:

    def calculate_checksum(file_path, algorithm, block_size):
        hash_function = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            block = file.read(block_size)
            while len(block) > 0:
                hash_function.update(block)
                block = file.read(block_size)
        return hash_function.hexdigest()

    checksum_list = []
    for root, dirs, files in os.walk(binary_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            checksum = calculate_checksum(file_path, algorithm, block_size)
            checksum_list.append(checksum)
    md5 = "".join(checksum_list)
    return md5

def write_config(config_path, platform, version, timestamp, md5) -> None:
    if os.path.isfile(config_path):
        with open(config_path, "r") as config_file:
            config_data = json.load(config_file)

        if f"{platform}" in config_data:
            config_data[f"{platform}"]["last_version"] = version
            config_data[f"{platform}"]["last_update"] = timestamp
            config_data[f"{platform}"]["last_md5"] = md5

        else:
            config_data[f"{platform}"] = {
                "last_version": version,
                "last_update": timestamp,
                "last_md5": md5
            }

        with open(config_path, "a") as config_file:
            json.dump(config_data, config_file, indent=4)

    else:
        with open(config_path, "w") as config_file:
            json.dump({f"{platform}": {
                "last_version": version,
                "last_update": timestamp,
                "last_md5": md5
            }}, config_file, indent=4)

def expose_binaries(*paths) -> None:
    for path in paths:
        os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])

#func prep_init() -> str:
platform = "win64" if platform.system() == "Windows" else (
        "mac-arm64" if platform.system() == "Darwin" else 
        "linux64")
binary_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
config_path = os.path.join(binary_path, platform, "chromefortesting_config.json")
platform_path = os.path.join(binary_path, platform)

@keyword("Initialise Chrome For Testing")
def main():

        # func assess_init() -> bool:
    if os.path.exists(config_path):

        # func read_config() -> (dict object?):
        try:
            with open(config_path, "r") as config_file:
                config_data = json.load(config_file)
                if platform in config_data:
                    last_version = config_data.get(platform, {}).get("last_version")
                    last_update = config_data.get(platform, {}).get("last_update")
                    last_md5 = config_data.get(platform, {}).get("last_md5")
                    initialised = not(generate_md5(os.path.join(binary_path, platform)) == last_md5)

        except json.JSONDecodeError:
            logging.error("Compromised configuration file detected. Rebuilding...")
            os.remove(config_path)
            initialised = False

    else:
        initialised = False

    if not initialised:
        logger.info("CfT: Setup initialisation...")

        # func fetch_updates(release_channel, platform, ...) -> (source objects?):
        response = requests.get(chromelabs_endpoint_url)
        if response.status_code == 200:
            current_version = response.json()["channels"]["Stable"]["version"]
            update_detected = int(current_version.replace(".", "")) > int(last_version.replace(".", "")) if initialised else False

            if not initialised or update_detected:

                # func obtain_binaries() -> (chrome binary, chromedriver binary):
                chrome_source = response.json()["channels"]["Stable"]["downloads"]["chrome"]
                chromedriver_source = response.json()["channels"]["Stable"]["downloads"]["chromedriver"]

                for chrome, chromedriver in zip(chrome_source, chromedriver_source):
                    if platform == chrome["platform"] == chromedriver["platform"]:

                        # func update_setup() -> None:
                        if os.path.exists(platform_path): shutil.rmtree(platform_path)
                        os.makedirs(os.path.join(binary_path, platform), exist_ok=True)
                        [os.remove(os.path.join(binary_path, file)) for file in os.listdir(binary_path) if file.endswith('.zip')]

                        chrome_source = requests.get(chrome["url"])
                        chromedriver_source = requests.get(chromedriver["url"])
                        chrome_zip = os.path.join(binary_path, f"chrome_{current_version}.zip")
                        chromedriver_zip = os.path.join(binary_path, f"chromedriver_{current_version}.zip")

                        # func put_binaries(chrome_source, chromedriver_source) -> (str, str):
                        with open(chrome_zip, "wb") as file: 
                            file.write(chrome_source.content)

                        with extended_ZipFile(chrome_zip, "r") as archive: 
                            archive.extractall(platform_path)
                        os.remove(chrome_zip)

                        with open(chromedriver_zip, "wb") as file: 
                            file.write(chromedriver_source.content)

                        with extended_ZipFile(chromedriver_zip, "r") as archive:
                            archive.extractall(platform_path)
                        os.remove(chromedriver_zip)
                        break

                    # func update_success_proceed() -> None:
                logger.info(f"CfT: New latest version in use: {current_version}. Initiating Robot Framework automation...")
                write_config(config_path, platform, current_version, str(datetime.datetime.now(datetime.timezone.utc)), generate_md5(platform_path))
                expose_binaries(os.path.join(platform_path, f"chrome-{platform}"), os.path.join(platform_path, f"chrome-{platform}"))

        else:
                # func update_fail_proceed() -> None:
            logger.warning("Update status check unsuccessful. Connectivity issues detected. Initiating Robot Framework automation...")
            expose_binaries(os.path.join(platform_path, f"chrome-{platform}"), os.path.join(platform_path, f"chromedriver-{platform}"))

    else:
        # func update_latest_proceed() -> None:
        logger.info("CfT: Initiating Robot Framework automation...")
        expose_binaries(os.path.join(platform_path, f"chrome-{platform}"), os.path.join(platform_path, f"chromedriver-{platform}"))

if __name__ == "__main__":
    main()