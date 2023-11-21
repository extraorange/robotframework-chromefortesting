from enum import Enum, auto

class State(Enum):
    INITIAL = auto()
    LATEST = auto()
    UPDATE = auto()
    NEWCHANNEL = auto()
    REPAIR = auto()