#!/usr/bin/env python3


from lib.core.arguments import Arguments
from lib.controller.puppet import Puppet
from lib.output.terminaloutput import TerminalOutput
import sys
import os

if sys.version_info < (3, 0):
    sys.stdout.write("Defaulter requires Python 3.x\n")
    sys.exit(1)

class Program(object):

    def __init__(self):
        self.path = (os.path.dirname(os.path.realpath(__file__)))
        self.arguments = Arguments(self.path)
        self.output = TerminalOutput()
        self.puppet = Puppet(self.path, self.arguments, self.output)


if __name__ == "__main__":
    main = Program()