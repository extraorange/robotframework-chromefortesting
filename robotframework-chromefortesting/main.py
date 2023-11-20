#!/usr/bin/env python
"""
robotframework-chromefortesting
Chrome for Testing (CfT) for Robot Framework

├── ${output_bin}                         +
│ ├── [platform]/                         +
│ │ ├── chrome-[platform]/                +
│ │ └── chromedriver-[platform]           +
│ └── chromefortesting_config.json        +

GitHub: https://github.com/extraorange/robotframework-chromefortesting

Disclaimer: Distributed as-is, without warranties or guarantees.

Author: extraorange (d***X)
Date: 13 Nov 2023
Version: 0.4 (pre-release)
License: GNU General Public License v3.0
"""

from robot.api.deco import keyword

from chromelabs import install_assets, ChromeAssets, locate_assets
from config import Config, State
from toolkit import reset_assets

@keyword("Initialise Chrome For Testing")
def main(channel: str = "Stable", path: str = "", headless: bool = False) -> str:

    config = Config(channel, path, headless)
    config.detect_state()

    if config.state is State.INITIAL or State.NEWCHANNEL is config.state or State.UPDATE is config.state:
        assets = install_assets(config)
        Config.write(config, assets)
        assets.expose_to_system
        return assets.parse_chrome_binary_path()

    elif State.REPAIR is config.state:
        reset_assets(config.path)
        assets = install_assets(config)
        Config.write(config, assets)
        assets.expose_to_system
        return assets.parse_chrome_binary_path()

    else: # State.LATEST is config.state
        assets = locate_assets(config)
        assets.expose_to_system
        return assets.parse_chrome_binary_path()

if __name__ == '__main__':
    main()