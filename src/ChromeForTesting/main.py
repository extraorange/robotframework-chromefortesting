#!/usr/bin/env python

# Chrome for Testing (CfT) for Robot Framework
# GitHub: https://github.com/extraorange/robotframework-chromefortesting
# Disclaimer: Distributed as-is, without warranties or guarantees.
# Author: extraorange
# Date: 13 Nov 2023
# Version: 0.9.3
# License: GNU General Public License v3.0

from .chromelabs import download_assets, load_local_assets, update_assets
from .config import Config, State

class ChromeForTesting:
    """
    Chrome for Testing (CfT) for Robot Framework
    Automated installation & initialization of Chrome For Testing binaries with 
    system autodetection, autoupdates, and integrity check for seamless operation.
    
    Usage: import as any other library in "Settings" section of .robot file.
    ```
    Library    ChromeForTesting    ${channel}=Stable    ${headless}=${False}
    ```
    Arguments:
        - ${channel}: Specify the desired version branch of CfT (Stable, Beta, Dev, Canary)
        - ${headless}: Configure CfT to run in headless mode for renderless testing.
    """
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

    def empty_keyword(self):
        pass
