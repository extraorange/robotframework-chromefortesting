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

Author: extraorange
Date: 13 Nov 2023
Version: 0.7 (pre-release)
License: GNU General Public License v3.0
"""

from typing import Optional
from robot.api.deco import keyword

from chromelabs import load_assets
from config import Config

@keyword("Initialise Chrome For Testing")
def main(channel: str = "Stable", path: Optional[str] = None, headless: bool = False) -> str:

    config = Config(channel, path, headless)
    assets = load_assets(config)
    config.write(assets)
    assets.expose_to_system()
    return assets.return_chrome_binary_path()

if __name__ == '__main__':
    main()