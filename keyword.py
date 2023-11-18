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

from typing import Union

from robot.api.deco import keyword

from main import init_setup, init_config, init_state

@keyword("Initialise Chrome For Testing")
def main(channel: str = "Stable", path: Union[None, str] = None) -> str:

    setup = init_setup(channel, path)
    config = init_config(setup)
    state = init_state(setup, config)

    if state is state.UPDATE:

    elif state is state.UPDATE:
        pass

    elif state.INITIAL is config.state:
        pass                # Log info: Initialising setup

    elif state.CHANNEL is config.state: 
        pass                # Log info: Initialising new channel setup
    
    elif state.REPAIR is config.state:
        pass                # Log info: Reinitializing Chrome for Testing setup


# # # Refactoring:

#     if downloading:
#         download()


#     elif initialise or downloading:
#         exit(2, os.path.join(output_bin, channel.lower(), f"chrome-{platform}"), os.path.join(output_bin, channel.lower(), f"chromedriver-{platform}"))

# elif initialise:
#     exit(1, os.path.join(output_bin, channel.lower(), f"chrome-{platform}"), os.path.join(output_bin, channel.lower(), f"chromedriver-{platform}"))

# else: 
#     exit(0)
    return Chrome.path

if __name__ == '__main__':
    main()