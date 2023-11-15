# robotframework-chromefortesting :ukraine:

![Version](https://img.shields.io/badge/version-0.3-%2392C444) ![Made in Ukraine](https://img.shields.io/badge/made_in_Ukraine-%23AF1717)

A minimalistic tool for seamless settup of Chrome for Testing (CfT) in Robot Framework.
For detailed information on CfT, refer to the official CfT documentation:

- [Chrome for Testing Documentation](https://developer.chrome.com/blog/chrome-for-testing/)
- [Google Chrome Labs - Chrome for Testing (CfT)](https://googlechromelabs.github.io/chrome-for-testing/)

## Overview

This script automates the installation and configuration of Chrome and Chromedriver for testing purposes. It ensures a consistent testing environment across different platforms.

_in progress..._

## Instalation

_in progress..._

## Usage
### In Robot Framework

```
Initialise Chrome For Testing    ${channel}    ${bin_path}
```
If channel is not provided -> default to ```STABLE```.

Directory tree upon keyword execution:
```
├── ${bin_path}                       +
│ ├── [platform]/                     +
│ │ ├── chrome-[platform]/            +
│ │ └── chromedriver-[platform]       +
│ └── chromefortesting_config.json    +
```

## Pre-release checklist

- [ ] Progress bar for downloads
- [ ] Robust platform detection.
- [ ] Detection of pre-exposed Chromedriver.
- [ ] All channels.
- [ ] Custom binary location.
- [ ] Explicit standalone logging.
- [ ] Logging within Robot Framework.
- [ ] Release to PyPl as a package.