#!/usr/bin/env python
'''
Chrome for Testing (CfT) for Robot Framework

*** Settings ***
Library    ChromeForTesting    ${channel}=stable    ${headless}=False

GitHub: https://github.com/extraorange/robotframework-chromefortesting

Disclaimer: Distributed as-is, without warranties or guarantees.

Author: extraorange
Date: 13 Nov 2023
Version: 0.91 (beta)
License: GNU General Public License v3.0
'''

from chromelabs import download_assets, load_local_assets, update_assets
from config import Config, State


class ChromeForTesting:
    def __init__(self, channel: str = "stable", headless: bool = False):

        config = Config(channel, headless)
        if config.state is State.LIVE:
            pass
        elif config.state in [State.INITIAL, State.NEWCHANNEL]:
            assets = download_assets(config)
            config.write(assets)
            assets.expose_to_system()
        elif config.state in [State.UPDATE, State.REPAIR]:
            assets = update_assets(config)
            config.write(assets)
            assets.expose_to_system()
        elif config.state is State.LATEST:
            assets = load_local_assets(config)
            assets.expose_to_system()
