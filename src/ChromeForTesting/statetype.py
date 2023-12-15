from enum import Enum, auto

class State(Enum):
    LIVE = auto()
    INITIAL = auto()
    LATEST = auto()
    UPDATE = auto()
    NEWCHANNEL = auto()
    REPAIR = auto()
