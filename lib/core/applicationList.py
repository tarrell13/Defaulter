# -*- coding: utf-8 -*-


class ApplicationList(object):

    def __init__(self, arguments, resources):

        self.resources = resources
        self.arguments = arguments
        # Initialize empty application and data dictionaries
        self.applications = {}
        self.data = {}

        # Gather modules
        self.modules = self.resources.modules

        # Execute application list creation
        self.applicationMakeBuild()
        self.applicationModelBuild()


    # Generate application dictionary with MAKE
    def applicationMakeBuild(self):

        for module in self.modules:
            if module not in self.applications:
                self.applications[module] = {}

    # Generate MODELS for each MAKE
    def applicationModelBuild(self):

        if self.arguments.custom:
            self.applications["custom"]["custom"] = []

        for make in self.modules:
            self.data = self.generateData(make)
            for config in self.data["STRUCTURE"]["CONFIGURATION"]:
                for model in config["MODELS"]:
                    self.applications[make][model] = []

                self.applications[make]["unknown"] = []

    # Open Module structure file
    def generateData(self, make):
            return self.resources.QueryApplicationModule(make)

    # Push tagged host to applicable application make and model for creation
    def appendHost(self, host_list):

        for host in host_list:

            if self.arguments.custom:
                self.applications["custom"]["custom"].append(host)
                continue

            for make, model in self.applications.items():
                if make is host.application_make:
                    if host.application_model.lower() == "unknown":
                        self.applications[make]["unknown"].append(host)
                    else:
                        for model, values in self.applications[make].items():
                            if model.lower() == host.application_model.lower():
                                self.applications[make][model].append(host)


