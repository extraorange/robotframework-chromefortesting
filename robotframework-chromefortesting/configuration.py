from json import JSONDecodeError
import os
from shutil import rmtree as remove
from typing import Optional

from asetup import Setup
from chromelabs import ChromeAssets, check_updates
from main import State
from toolkit import get_hash


class Config():
    version: Optional[str] = None
    timestamp: Optional[str] = None
    md5: Optional[str] = None
    state: State = State.UPDATE


def load_config(config_path: str) -> dict:
    try:
        with open(config_path, "r") as config_file:
            return json.load(config_file)

    except FileNotFoundError:
        return {}

    except JSONDecodeError: 
        remove_config(config_path)
        return {}

def create_config(setup: Setup, chrome: ChromeAssets):
        with open(setup.config_path, "w") as json_file:
                json.dump({
                    setup.platform: {
                        setup.channel: {
                            "last_version": version,
                            "last_update": timestamp,
                            "last_md5": md5
                        }
                    }
                }, json_file, indent=4)


def update_config(config_path: str, chrome: ChromeAssets):
        if platform in config_data and channel in config_data[platform]:
            config_data[platform][channel].update({
                                                "last_version": version,
                                                "last_update": timestamp,
                                                "last_md5": md5
                                            })

        else:
            config_data[platform][channel] = {
                "last_version": version,
                "last_update": timestamp,
                "last_md5": md5
            }

        with open(config_path, "w") as json_file:
                json.dump(config_data, json_file, indent=4)

def remove_config(config_path: str) -> None:
    remove(config_path)

    




def get_config(config_json: dict) -> Config:
    load_config
    channel_dict = config_json[setup.platform].get(setup.channel, {})
    if channel_dict:
        md5 = channel_dict.get("last_md5")

        if get_hash(Setup.channel_path) == md5:
            version = channel_dict.get("last_version")

            return Config(
                version=version,
                timestamp=channel_dict.get("last_update"), 
                md5=md5, 
                state=State.UPDATE if check_updates(setup.channel, version) else State.LATEST
                )

        else:
            return Config(
            state=State.REPAIR
            )

    else:
        return Config(
            state=State.CHANNEL
            )

    # if detect_config(setup.config_path):
    #     config_json = load_config(setup.config_path)
    #     return parse_config_state(config_json)

    # else:
    #     return Config(
    #         state=State.INITIAL
    #     )