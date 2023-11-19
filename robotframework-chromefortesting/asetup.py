import os
from platform import system

class Setup():     
    def __init__(self, channel: str, path: str, headless: bool) -> None:
        self.channel: str = self.process_channel(channel)
        self.path: str = self.process_path(path)
        self.headless: bool = headless  # Write headless behaviour

    @property
    def platform(self) -> str: #! Improve detection: linux64, mac-arm64, mac-x64, win32, win64
        platforms = {"Windows": "win64", "Darwin": "mac-arm64", "Linux": "linux64"}
        return platforms.get(system(), "")

    @staticmethod
    def process_channel(channel: str) -> str:
        #! Add channel validation
        return channel.lower().capitalize()

    @staticmethod
    def process_path(path: str) -> str:
        if path is False: return os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        elif os.path.exists(path): return path
        else: return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

    @property
    def config_path(self) -> str:
        return os.path.join(self.path, "cft_config.json")

    @property
    def channel_path(self) -> str:
        return os.path.join(self.path, self.channel.lower())