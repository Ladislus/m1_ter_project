from CLIParser import parse
from ArgumentPrinter import print_parameters

if __name__ == '__main__':
    command_lign_parameters: dict = parse()
    print_parameters(command_lign_parameters)

