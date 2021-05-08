from enum import Enum, auto


class Params(Enum):
    FAMILY = auto()
    ELEMENTS = auto()
    VERBOSE = auto()
    QUIET = auto()
    LOCAL_ONLY = auto()
    REMOTE_ONLY = auto()
    OPENKIM_ONLY = auto()
    NIST_ONLY = auto()
    LOAD_NIST = auto()
    LOAD_KIM = auto()