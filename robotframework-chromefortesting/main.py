from enum import Enum, auto

from asetup import Setup
from chromelabs import check_updates, install_chromefortesting
from configuration import Config, create_config, init_config, update_config
from toolkit import expose_binaries

class State(Enum):
    INITIAL = auto()
    CHANNEL = auto()
    UPDATE = auto()
    REPAIR = auto()
    LATEST = auto()


def state(setup: Setup, config: Config, url: str) -> Config:

    if State.INITIAL is config.state or State.REPAIR is config.state:
        install_chromefortesting()
        create_config()

    elif State.UPDATE is config.state or State.CHANNEL is config.state:
        install_chromefortesting()
        update_config()

    else:
        pass