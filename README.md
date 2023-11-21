# robotframework-chromefortesting :ukraine:

![Version](https://img.shields.io/badge/version-0.8.3-%2392C444) ![Made in Ukraine](https://img.shields.io/badge/made_in_Ukraine-%23AF1717)

The only extension for seamless setup of Chrome for Testing (CfT) in and within Robot Framework.

For detailed information on CfT, refer to the official CfT documentation:

- [Chrome for Testing Documentation](https://developer.chrome.com/blog/chrome-for-testing/)
- [Google Chrome Labs - Chrome for Testing (CfT)](https://googlechromelabs.github.io/chrome-for-testing/)

## :book: Overview

:tophat: [**Before proceeding check out release checklist.**](#clipboard-checklist)

This module provides a conveniet keyword that takes care of automated installation and configuration of specific Chromium flavour: **Chrome for Testing**. Dynamically ensures a consistent automation testing environment across multiple platforms, by encapsulation of automatic browser infrastructure setup.

## :package: Instalation

_is being written..._

## :hammer: Usage

In your Robot Framework script:

```robot

Initialise Chrome For Testing    ${channel}=stable    ${path}=None
Open Browser    ...    browser=chrome
```

Initialisation tree if custom `${path}` provided:

```
 ${output_bin}                         +
  ├── [channel]/                       +
  │ ├── chrome-[platform]/             +
  │ └── chromedriver-[platform]/       +
  └── chromefortesting_config.json     +
```

_You might want to include your custom bin folder in your .gitignore..._

### :warning: Oi, Windows!

Due to Chromedriver server-like nature, if Google Chrome is installed on Windows -> Chromedriver will attempt to communicate to Google Chrome default binary install location `C:\Program Files\Google\Chrome\Application\` uncoditionally, preeceding system-wide $PATH look-ups and their priority order or .venv activation $PATH gatekeeping.

Alas, this initiation takes precedence over system-wide `%PATH%` executable path and any kind of virtual environment activation `%PATH%` control.

Thus, to CfT binary recognition, consider the following strategies based on your specific use case, context, workflow, or pipeline:

0. [**Ditch Google Chrome.**](https://en.wikipedia.org/wiki/Nothing_to_hide_argument) -> **OK** for CI/CD agents & containers, humankind.
1. :bulb: **Recommended** :bulb: Capture module keyword output & provide with `Open Browser` options:

```robot

 ${binary_location}    Initialise Chrome For Testing
 ${options}    Set Variable    add_argument("--binary-location=${binary_location}")
 Open Browser    ...    browser=chrome    option=${options}
```

2. Select `Beta` instead of `Stable` channel (or any other).
   Version divergence against consumer release of Google Chrome will result in non-compatible binary bypass. -> **OK** for anticipatory automated testing, smart.
3. Rename default Google Chrome executable: `chrome.exe` -> `googlechrome.exe` -> **OK**, obscure.

## :clipboard: Checklist

- [ ] complete platform detection
- [ ] chrome binary return support
- [ ] update schedule setter
- [ ] headless chrome support
- [ ] explicit Robot Framework logging
- [ ] progress bar for downloads
- [ ] complete error handling
