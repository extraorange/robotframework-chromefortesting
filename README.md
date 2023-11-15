# robotframework-chromefortesting :ukraine:

![Version](https://img.shields.io/badge/version-0.4-%2392C444) ![Made in Ukraine](https://img.shields.io/badge/made_in_Ukraine-%23AF1717)

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

In your usual .robot script:

```
${binary_path}    Initialise Chrome For Testing    ${channel}    ${binary_path}
```

If unprovided:
```channel``` -> ```STABLE```, ```binary_path``` -> ```to be done```

Directory tree upon keyword execution:
```
├── ${bin_path}                       +
│ ├── [platform]/                     +
│ │ ├── chrome-[platform]/            +
│ │ └── chromedriver-[platform]       +
│ └── chromefortesting_config.json    +
```

### Oi, Windows! :warning:
Due to Chromedriver server-like nature, if Google Chrome is installed on Windows -> Chromedriver will attempt to communicate to Google Chrome default binary install location ```C:\Program Files\Google\Chrome\Application\``` uncoditionally, preeceding system-wide $PATH look-ups and their priority order or .venv activation $PATH gatekeeping.

In order to "harden" CfT binary recognition, consider the following depending on your usecase/context/workflow/pipeline:

0. [_Ditch Google Chrome._][https://en.wikipedia.org/wiki/Nothing_to_hide_argument] -> OK for CI/CD agents & containers, humankind.
1. :bulb: *_Recommended._* :bulb: Capture keyword output ```${binary_path}``` & provide with ```Open Browser    ...    options``` keyword. -> OK.
2. Select ```Beta``` instead of ```Stable``` channel. Version divergence against consumer release of Google Chrome will result devergent binary bypass. -> OK for multi-platform teams and future-ready automation testing, convenient.
3. Rename default Google Chrome executable: ```chrome.exe``` -> ```googlechrome.exe```. -> OK for inidividuals, lazy.

## Release checklist

- [ ] Progress bar for downloads
- [ ] Robust platform detection
- [ ] Detection of pre-exposed Chromedrivers
- [ ] Dynamic channels support
- [ ] Better default & custom binary location
- [ ] Explicit Robot Framework logging
- [ ] Release to PyPl as a package