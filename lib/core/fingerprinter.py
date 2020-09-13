# -*- coding: utf-8 -*-

import urllib.parse
import re
import sys


class Fingerprinter(object):

    def __init__(self, host_list, application_list, output, arguments, modules=None):
        self.host_list = host_list
        self.application_list = application_list
        self.output = output
        self.arguments = arguments

        """ TESTING UNDER Enumerate() """
        # self.enumerate_vendor(modules)
        # self.enumerate_model(modules)

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

    def enumerate_vendor(self, modules):
        """ Updated FingerPrint Using version 2 Configs """

        for host in self.host_list:
            for module in modules:
                """ Match Any Specified Cookies """
                if module.vendor_prints.cookies:
                    if host.response.cookies.values():
                        for response_cookie in host.response.cookies.values():
                            for finger_cookie in module.vendor_prints.cookies:
                                if re.search(str(urllib.parse.quote(finger_cookie)), str(response_cookie), re.IGNORECASE):
                                    host.vendor_name = module.vender_name
                                    module.hosts.append(host)
                                    break

                if module.vendor_prints.page_source:
                    if re.search(module.vendor_prints.page_source, host.response.content().decode(), re.IGNORECASE):
                        host.vendor_name = module.vender_name
                        module.hosts.append(host)
                        break

    def enumerate_model(self, modules):
        """ Enumerate Model After Mapping Make """
        for module in modules:
            if module.hosts:
                for config in module.vendor_configs:
                    for model in config.models:
                        pass
