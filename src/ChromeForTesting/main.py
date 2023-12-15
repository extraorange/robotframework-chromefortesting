#!/usr/bin/env python
'''
Chrome for Testing (CfT) for Robot Framework

*** Settings ***
Library    ChromeForTesting

*** Keywords***
Open Chrome Browser
    Initialise Chrome For Testing    ${channel}=stable    ${path}=None    ${headless}=False
    Open Browser    ...    browser=chrome

GitHub: https://github.com/extraorange/robotframework-chromefortesting

Disclaimer: Distributed as-is, without warranties or guarantees.

Author: extraorange
Date: 13 Nov 2023
Version: 0.8.92 (beta)
License: GNU General Public License v3.0
'''

from typing import Optional

from robot.api.deco import keyword

from chromelabs import download_assets, load_local_assets, update_assets
from config import Config
from statetype import State

@keyword("Initialise Chrome For Testing")
def main(channel: str = "Stable", path: Optional[str] = None, headless: bool = False):

    config = Config(channel, path, headless)
    if config.state is State.LIVE:
        pass
    if config.state in [State.INITIAL, State.NEWCHANNEL]:
        assets = download_assets(config)
        config.write(assets)
        assets.expose_to_system()
        return assets.return_chrome_binary_path()
    elif config.state in [State.UPDATE, State.REPAIR]:
        assets = update_assets(config)
        config.write(assets)
        assets.expose_to_system()
        return assets.return_chrome_binary_path()
    elif config.state is State.LATEST:
        assets = load_local_assets(config)
        assets.expose_to_system()
        return assets.return_chrome_binary_path()

if __name__ == '__main__':
    main()
