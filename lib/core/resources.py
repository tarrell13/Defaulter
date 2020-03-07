# -*- coding: utf-8 -*-

import os
import sys
import json


class Resources(object):

    def __init__(self, path, arguments, output):
        self.path = path
        self.arguments = arguments
        self.output = output

        self.modules = []
        self.module = {}

        # Validation of all modules
        if self.arguments.validation and self.arguments.modules == "all":
            self.RetrieveModules()
            sys.exit()
        # Validation of specified modules
        elif self.arguments.validation and self.arguments.modules:
            self.RetrieveSpecificModules(self.arguments.modules)
            sys.exit()

        if self.arguments.modules == "all":
            self.RetrieveModules()
        else:
            self.RetrieveSpecificModules(self.arguments.modules)


    # Pulls all the modules into the modules array from modules directory
    def RetrieveModules(self):

        for file in os.listdir(self.path + "/lib/modules"):
            file = file.replace(".json","")
            try:
                if self.ValidateModuleFile(file):
                    if self.arguments.validation:
                        self.output.InformationalOutput(module=file)
                        continue
                    else:
                        self.modules.append(file)
                else:
                    self.output.errorOutput(module=file)
            except json.decoder.JSONDecodeError:
                self.output.errorOutput(module=file)
            except FileNotFoundError:
                self.output.errorOutput(file=file)

        return

    # Queries selected modules
    def RetrieveSpecificModules(self, modules):

        if self.arguments.custom:
            self.modules.append("custom")
            return

        for module in modules:
            try:
                if self.ValidateModuleFile(module):
                    if self.arguments.validation:
                        self.output.InformationalOutput(module=module)
                        continue
                    else:
                        self.modules.append(module)
                else:
                    self.output.errorOutput(module=module)
            except json.decoder.JSONDecodeError:
                self.output.errorOutput(module=module)
            except FileNotFoundError:
                self.output.errorOutput(file=module)

        return

    # Return application module
    def QueryApplicationModule(self, module):

        if self.arguments.custom:
            self.module = json.loads(open(self.path+"/template.json", "r").read())
            return self.module

        self.module = json.loads(open(self.path+"/lib/modules/%s.json" %module, "r").read())
        return self.module

    # Returns the application authentication structure based on model
    def QueryApplicationModelStruct(self, model):
        for build in self.module["STRUCTURE"]["CONFIGURATION"]:
            if model in build["MODELS"]:
                return build
        return

    # Self validation check before starting application creation process
    def ValidateModuleFile(self, module):

        self.QueryApplicationModule(module)

        if "STRUCTURE" not in self.module:
            return False

        if "FINGERPRINTS" not in self.module["STRUCTURE"] and "CONFIGURATION" not in self.module["STRUCTURE"]:
            return False

        for config in range(len(self.module["STRUCTURE"]["CONFIGURATION"])):
            if "MODELS" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "AUTHENTICATION" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "URI" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "PARAMETERS" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "SUCCESS_TOKENS" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "REDIRECTION" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "TOKEN_URI" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "FAILURE_TOKENS" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "THRESHOLD" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "COOKIES" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "USERNAMES" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "PASSWORDS" not in self.module["STRUCTURE"]["CONFIGURATION"][config]:
                return False

            if "GET" not in self.module["STRUCTURE"]["CONFIGURATION"][config]["URI"]:
                return False

            if "POST" not in self.module["STRUCTURE"]["CONFIGURATION"][config]["URI"]:
                return False

            if ("USER_PARAMETER" not in self.module["STRUCTURE"]["CONFIGURATION"][config]["PARAMETERS"] and
                "PASS_PARAMETER" not in self.module["STRUCTURE"]["CONFIGURATION"][config]["PARAMETERS"] and
                "DYNAMIC" not in self.module["STRUCTURE"]["CONFIGURATION"][config]["PARAMETERS"] and
                "STATIC" not in self.module["STRUCTURE"]["CONFIGURATION"][config]["PARAMETERS"]):
                return False

        return True