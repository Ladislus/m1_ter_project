from argparse import ArgumentParser
from enum import Enum, auto


class Params(Enum):
    FAMILLY = auto()
    ELEMENTS = auto()
    VERBOSE = auto()
    QUIET = auto()
    LOCAL_ONLY = auto()
    REMOTE_ONLY = auto()
    OPENKIM_ONLY = auto()
    NIST_ONLY = auto()


def parse() -> dict:
    parser: ArgumentParser = ArgumentParser()

    ## Parameters ##

    parser.add_argument("familly",
                        help="The familly of atommic interaction",
                        action="store",
                        type=str)

    parser.add_argument("elements",
                        help="List of the elements that are to interact",
                        action="extend",
                        type=str,
                        nargs="+")

    ## Options ##

    # Verbosity options
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-v", "--verbose",
                                 required=False,
                                 help="Activate verbose output",
                                 action="store_true")
    verbosity_group.add_argument("-q", "--quiet",
                                 required=False,
                                 help="Disable output",
                                 action="store_true")

    # Location options
    location_group = parser.add_mutually_exclusive_group()
    location_group.add_argument("-l", "--local-only",
                                dest="local",
                                required=False,
                                help="Looking for potential files only in the local database",
                                action="store_true")
    location_group.add_argument("-r", "--remote-only",
                                dest="remote",
                                required=False,
                                help="Looking for potential files only in the remote database",
                                action="store_true")

    # Database options
    database_group = parser.add_mutually_exclusive_group()
    database_group.add_argument("-k", "--openkim-only",
                                dest="kim",
                                required=False,
                                help="Looking for potential files only in the OpenKIM remote database",
                                action="store_true")
    database_group.add_argument("-n", "--nist-only",
                                dest="nist",
                                required=False,
                                help="Looking for potential files only in the NIST remote database",
                                action="store_true")

    args = parser.parse_args()

    return {
        Params.FAMILLY: args.familly,
        Params.ELEMENTS: args.elements,
        Params.VERBOSE: args.verbose,
        Params.QUIET: args.quiet,
        Params.LOCAL_ONLY: args.local,
        Params.REMOTE_ONLY: args.remote,
        Params.OPENKIM_ONLY: args.kim,
        Params.NIST_ONLY: args.nist
    }