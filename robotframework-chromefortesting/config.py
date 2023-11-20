from enum import Enum, auto
import json
import os
from platform import system
import shutil
from typing import Optional

from toolkit import get_hash
from chromelabs import check_updates


class State(Enum):
    INITIAL = auto()
    LATEST = auto()
    UPDATE = auto()
    NEWCHANNEL = auto()
    REPAIR = auto()


class ChromeAssets():
    def __init__(self, chrome_path: str, chromedriver: str, version: Optional[str] = None, timestamp: Optional[str] = None, md5: Optional[str] = None) -> None:
        self.chrome: str = chrome_path
        self.chromedriver: str = chromedriver
        self.version: Optional[str] = version
        self.timestamp: Optional[str] = timestamp
        self.md5: Optional[str] = md5

    def expose_to_system(self) -> None:
        for path in [self.chrome, self.chromedriver]:
            os.environ['PATH'] = os.pathsep.join([os.path.abspath(path), os.environ.get('PATH', '')])

    def parse_chrome_binary_path(self) -> str:
        #! Windows path processing for Robot Framework
        return self.chrome


class Config():
    def __init__(self, channel: str, path: Optional[str], headless: bool) -> None:
        self.platform
        self.channel: str = self.process_channel(channel)
        self.path: str = self.process_path(path)
        self.headless: bool = headless
        self.channel_path
        self.config_path
        self.config_data

    @property
    def platform(self) -> str: #! Improve detection: linux64, mac-arm64, mac-x64, win32, win64
        platforms = {"Windows": "win64", "Darwin": "mac-arm64", "Linux": "linux64"}
        return platforms.get(system(), "")

    @staticmethod
    def process_channel(channel: str) -> str:
        #! Add channel validation
        return channel.lower().capitalize()

    @staticmethod
    def process_path(path) -> str: #! Improve dynamic output folder
        if not path: return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        elif os.path.exists(path): return path
        else: return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

    @property
    def channel_path(self) -> str:
        return os.path.join(self.path, self.channel.lower())

    @property
    def config_path(self) -> str:
        return os.path.join(self.path, "cft_config.json")

    @property
    def config_data(self) -> dict:
        try:
            with open(self.config_path, "r") as config_file:
                return json.load(config_file)
                
        except FileNotFoundError:
            return {}

        except json.JSONDecodeError: 
            shutil.rmtree(self.config_path)
            shutil.rmtree(self.path)
            return {}

    def detect_state(self) -> None:

        if self.config_data:
            channel_data = self.config_data[self.platform].get(self.channel, {})
            if channel_data:
                md5 = channel_data.get("last_md5")

                if get_hash(self.channel_path) == md5:

                    if check_updates(self.channel, channel_data.get("last_version")):
                        self.state = State.UPDATE
                        
                    else:
                        self.state = State.LATEST

                else:
                    self.state = State.REPAIR

            else:
                self.state = State.NEWCHANNEL

        else:
            self.state = State.INITIAL

    def write(self, assets: ChromeAssets) -> None:
        if self.platform in self.config_data:
            if self.channel in self.config_data[self.platform]:
                self.config_data[self.platform][self.channel].update({
                    "last_version": assets.version,
                    "last_update": assets.timestamp,
                    "last_md5": assets.md5
                })

            else:
                self.config_data[self.platform][self.channel] = {
                    "last_version": assets.version,
                    "last_update": assets.timestamp,
                    "last_md5": assets.md5
                }

        else:
            self.config_data[self.platform] = {
                self.channel: {
                    "last_version": assets.version,
                    "last_update": assets.timestamp,
                    "last_md5": assets.md5
                }
            }

        with open(self.config_path, "w") as json_file:
            json.dump(self.config_data, json_file, indent=4)