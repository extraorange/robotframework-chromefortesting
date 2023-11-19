import json
import os
import platform

import requests
from requests.models import Response
from typing import Optional, Union
from asetup import Setup
from toolkit import PureUnzip


class ChromeLabsService():
    def __init__(self, setup: Setup) -> None:
        self.url: str = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
        self.platform: str = setup.platform
        self.channel: str = setup.channel
        self.channel_path: str = setup.channel_path
        self.headless: bool = setup.headless

    @property
    def response(self) -> Union[Response, None]:
        response = requests.get(self.url)
        return response if response.status_code == 200 else None

    def check_updates(self, current_version: str) -> bool:
        if self.response: 
            remote_version = self.response.json()["channels"][self.channel]["version"]
            return current_version != remote_version
        else: 
            return False

    def install_binaries(self, platform:channel: str, output_bin: str, headless: bool) -> ChromeForTesting:
        if self.response:
            if headless: chrome_pool = self.response.json()["channels"][channel]["downloads"]["chrome-headless-shell"]
            else: chrome_pool = self.response.json()["channels"][channel]["downloads"]["chrome"]
            chromedriver_pool = self.response.json()["channels"][channel]["downloads"]["chromedriver"]

            for chrome, chromedriver in zip(chrome_pool, chromedriver_pool):
                if platform == chrome["platform"] == chromedriver["platform"]:

        chrome = response.json()["channels"][channel]["downloads"]["chrome"]
        chromedriver = response.json()["channels"][channel]["downloads"]["chromedriver"]

        
        channel_dir = os.path.join(output_bin, channel.lower())

        if os.path.exists(channel_dir): shutil.rmtree(channel_dir)
        os.makedirs(channel_dir, exist_ok=True)
        [os.remove(os.path.join(output_bin, file)) for file in os.listdir(output_bin) if file.endswith('.zip')]

        chrome_source = requests.get(chrome["url"])
        chromedriver_source = requests.get(chromedriver["url"])

        chrome_zip = os.path.join(output_bin, f"chrome_{current_version}.zip")
        chromedriver_zip = os.path.join(output_bin, f"chromedriver_{current_version}.zip")

    class ChromeForTesting():
        def __init__(self) -> None:
            self.chrome: str
            self.chromedriver: str
            version: str
            timestamp: str
            md5: str


            def get_chrome(self) -> str:
                return self.chrome

            def get_chromedriver(self) -> str:
                return self.chromedriver

            def expose_binaries(*paths: str) -> str:
                for path in paths:
                    os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])
                return




    # def 
    # with open(chrome_zip, "wb") as file:
    #     file.write(chrome_source.content)

    # with PureUnzip(chrome_zip, "r") as archive:
    #     archive.extractall(channel_dir)
    # os.remove(chrome_zip)

    # with open(chromedriver_zip, "wb") as file:
    #     file.write(chromedriver_source.content)

    # with PureUnzip(chromedriver_zip, "r") as archive:
    #     archive.extractall(channel_dir)
    # os.remove(chromedriver_zip)
    # break