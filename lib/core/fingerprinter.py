# -*- coding: utf-8 -*-

import re
import sys

class Fingerprinter(object):

    def __init__(self, host_list, application_list, output, arguments):
        self.host_list = host_list
        self.application_list = application_list
        self.output = output
        self.arguments = arguments

        # Fingerprint Targets
        self.fingerprint()

    def fingerprint(self):

        for host in self.host_list:

            if self.arguments.custom:
                host.application_make= "custom"
                host.application_model = "custom"
                self.output.InformationalOutput(fingerprint=host)
                continue

            for make, configs in self.application_list.items():
                model_counter = 0
                if re.search(str(make).lower(), str(host.sample)):
                    host.application_make = make
                    for model, values in self.application_list[make].items():

                        if re.search(str(model.lower()), str(host.sample)):
                            host.application_model = model
                            if self.arguments.verbose or self.arguments.only_fingerprint:
                                self.output.InformationalOutput(fingerprint=host)
                            break
                        elif model_counter < len(configs):

                            model_counter += 1

                            if model_counter == len(configs):
                                host.application_model = "unknown"
                                if self.arguments.verbose or self.arguments.only_fingerprint:
                                    self.output.InformationalOutput(fingerprint=host)
                            else:
                                continue

        if self.arguments.only_fingerprint:
            sys.exit()

    def FingerUpdate(self):
        """ Updated Finger print sing response headers test """
        pass