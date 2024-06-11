from enum import Enum, auto
import json
import os
from platform import system
import shutil

from .chromelabs import check_updates
from .toolkit import get_hash

class State(Enum):
    LIVE = auto()
    INITIAL = auto()
    LATEST = auto()
    UPDATE = auto()
    NEWCHANNEL = auto()
    REPAIR = auto()

class Config():
    def __init__(self, channel: str, headless: bool):
        self.platform: str = self.detect_platform()
        self.channel: str = self.process_channel(channel)
        self.path: str = self.process_path()
        self.headless: bool = headless
        self.channel_path: str = self.process_channel_path()
        self.config_path: str = self.process_config_path()
        self.config_data: dict = self.load_config_data()
        self.state: State = self.initialise_state()

    def detect_platform(self) -> str: #! Improve detection: linux64, mac-arm64, mac-x64, win32, win64
        platforms = {"Windows": "win64", 
                     "Darwin": "mac-arm64", 
                     "Linux": "linux64"}
        return platforms.get(system(), "")

    def process_channel(self, channel: str) -> str:
        return channel.lower().capitalize()

    def process_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")

    def process_channel_path(self) -> str:
        return os.path.join(self.path, self.channel.lower())

    def process_config_path(self) -> str:
        return os.path.join(self.path, "cft_config.json")

    def load_config_data(self) -> dict:
        try:
            with open(self.config_path, "r") as config_file:
                return json.load(config_file)
        except (FileNotFoundError, json.JSONDecodeError):
            if os.path.exists(self.path): shutil.rmtree(self.path)
            return {}

    def initialise_state(self) -> State:
        if self.path in os.environ['PATH']: 
            return State.LIVE
        elif self.config_data:
            channel_data = self.config_data[self.platform].get(self.channel, {})
            if channel_data:
                md5 = channel_data.get("last_md5")
                if get_hash(self.channel_path) == md5:
                    if check_updates(self.channel, channel_data.get("last_version")):
                        return State.UPDATE
                    else:
                        return State.LATEST
                else:
                    return State.REPAIR
            else:
                return State.NEWCHANNEL
        else:
            return State.INITIAL

    def write(self, assets) -> None:
        if self.state is State.LATEST:
            return
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
