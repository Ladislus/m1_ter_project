from CLIParser import Params


def print_parameters(parameters: dict):
    if not parameters[Params.QUIET]:
        print("Interaction familly: {}".format(parameters[Params.FAMILLY]))
        print("Elements interacting: [ {} ]".format(", ".join(parameters[Params.ELEMENTS])))

        if parameters[Params.VERBOSE]:
            print("Verbose mode activated")
            if parameters[Params.LOCAL_ONLY]:
                print("Local only")
            elif parameters[Params.REMOTE_ONLY]:
                print("Remote only")
            else:
                print("Default search")

            if not parameters[Params.LOCAL_ONLY]:
                if parameters[Params.NIST_ONLY]:
                    print("Fectching NIST database")
                elif parameters[Params.OPENKIM_ONLY]:
                    print("Fectching OpenKIM database")
                else:
                    print("All databases")
            if parameters[Params.LOAD_KIM]:
                print("Loading all OpenKIM database")
            if parameters[Params.LOAD_NIST]:
                print("Loading all NIST database")
