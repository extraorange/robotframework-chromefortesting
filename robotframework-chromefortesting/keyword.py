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

from typing import Optional

from robot.api.deco import keyword

from configuration import init_config
from asetup import Setup
from chromelabs import ChromeAssets

@keyword("Initialise Chrome For Testing")
def main(channel: str = "Stable", path: str = "", headless: bool = False) -> str:

    setup = Setup(channel, path, headless)
    config = init_config(setup)




    return ChromeAssets.path

if __name__ == '__main__':
    main()