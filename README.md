# robotframework-chromefortesting :ukraine:

![Version](https://img.shields.io/badge/version-0.9.1-%2392C444) ![Made in Ukraine](https://img.shields.io/badge/made_in_Ukraine-%23AF1717)

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
Library    ChromeForTesting

*** Test Cases ***
Open page
    Open Chrome Browser    https://en.wikipedia.org/wiki/Grapefruit

*** Keywords ***
Open Chrome Browser    ${url}
    # Create your own custom browser/page opener and adjust further if required
    Initialise Chrome For Testing    ${channel}=stable    ${path}=None    ${headless}=False
    Open Browser    ${url}    browser=chrome
```

### :warning: Oi, Windows!

On Windows Chromedriver will attempt to access Google Chrome default binary install location `C:\Program Files\Google\Chrome\Application\` uncoditionally.
Alas, such attempt of access takes precedence over system-wide `%PATH%` executable path and any kind of virtual environment activation `%PATH%` control.
Thus, to harden only CfT binary recognition, consider the following strategies based on your specific use case, context, workflow, or pipeline:

0. [Ditch Google Chrome](https://en.wikipedia.org/wiki/Nothing_to_hide_argument) -> **OK** for CI/CD agents & containers, humankind.
1. :bulb: Capture module keyword output & provide with `Open Browser` options:

```robot
*** Keywords ***
Open Chrome Browser    ${url}
    ${binary_location}    Initialise Chrome For Testing    ${channel}=stable
    ${options}    Set Variable    add_argument("--binary-location=${binary_location}")
    Open Browser    ${url}    chrome    options=${options}
```

2. Select `Beta` instead of `Stable` channel (or any other).
   Version divergence against consumer release of Google Chrome will result in non-compatible binary bypass. -> **OK** for anticipatory automated testing, smart.
3. Rename default Google Chrome executable: `chrome.exe` -> `googlechrome.exe` -> **OK**, obscure.
