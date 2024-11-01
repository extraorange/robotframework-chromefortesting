# robotframework-chromefortesting :ukraine:

![Version](https://img.shields.io/badge/version-0.9.5-%2392C444)

The only library for seamless setup of Chrome for Testing (CfT) in and within Robot Framework.

For detailed information on CfT, refer to the official CfT documentation:

- [Chrome for Testing Documentation](https://developer.chrome.com/blog/chrome-for-testing/)
- [Google Chrome Labs - Chrome for Testing (CfT)](https://googlechromelabs.github.io/chrome-for-testing/)

## :book: Overview

This library provides an automated installation and initialisation of **Chrome for Testing**. 
Dynamically ensures a consistent automation testing environment across multiple platforms.
Safeguarded for automatical update and repair.

## :package: Instalation

```shell
pip install robotframework-chromefortesting
```

It is _highly recommended_ to use a virtual environment.

## :hammer: Usage

In your Robot Framework script:

```robot
*** Settings ***
Library    ChromeForTesting    ${channel}=Stable    ${headless}=${False}
```
