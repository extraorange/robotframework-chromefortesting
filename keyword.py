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

from main import get_setup, read_config

@keyword("Initialise Chrome For Testing")
def main(channel: str = "Stable", path: Union[None, str] = None) -> str:

    setup_data = get_setup(channel, path)
    initialise = assess_init(read_config(setup_data))

    return "string"

# # # Refactoring:

# response = requests.get(chromelabs_endpoint_url)
# if (initialise and response.status_code == 200) or (not initialise and response.status_code == 200):
#     current_version = response.json()["channels"][channel]["version"]
#     downloading = True if not initialise else (int(current_version.replace(".", "")) > int(last_version.replace(".", "")))
#     # TBD: Log: detected update

#     if downloading:
#         download()


#     elif initialise or downloading:
#         exit(2, os.path.join(output_bin, channel.lower(), f"chrome-{platform}"), os.path.join(output_bin, channel.lower(), f"chromedriver-{platform}"))

# elif initialise:
#     exit(1, os.path.join(output_bin, channel.lower(), f"chrome-{platform}"), os.path.join(output_bin, channel.lower(), f"chromedriver-{platform}"))

# else: 
#     exit(0)

if __name__ == '__main__':
    main()