# robotframework-chromefortesting :ukraine:

![Version](https://img.shields.io/badge/version-0.9.3-%2392C444)

The only extension for seamless setup of Chrome for Testing (CfT) in and within Robot Framework.

For detailed information on CfT, refer to the official CfT documentation:

- [Chrome for Testing Documentation](https://developer.chrome.com/blog/chrome-for-testing/)
- [Google Chrome Labs - Chrome for Testing (CfT)](https://googlechromelabs.github.io/chrome-for-testing/)

## :book: Overview

:tophat: [**Before proceeding check out release checklist**](#clipboard-checklist)

This module provides a conveniet keyword that takes care of automated installation and configuration of specific Chromium flavour: **Chrome for Testing**. Dynamically ensures a consistent automation testing environment across multiple platforms, by encapsulation of automatic browser infrastructure setup.

## :package: Instalation

```shell
pip install robotframework-chromefortesting
```

It is _highly recommended_ to use a virtual environment (.venv) for achieving best reliability.

## :hammer: Usage

In your Robot Framework script:

```robot
*** Settings ***
Library    ChromeForTesting    ${channel}=Stable    ${headless}=${False}
```
