# -*- coding: utf-8 -*-

from lib.core.fingerprinter import Fingerprinter
from lib.core.applicationList import ApplicationList
from lib.core.resources import Resources
from lib.core.application import Application
from lib.core.authenticator import Authenticator
from lib.core.host import Host
from seleniumrequests import Firefox
import selenium
import threading
import sys


MAYOR_VERSION = 0
MINOR_VERSION = 0
REVISION = 0

VERSION = {
    "MAYOR_VERSION": MAYOR_VERSION,
    "MINOR_VERSION": MINOR_VERSION,
    "REVISION": REVISION
}

host_objects = []
application_list = []


class Puppet(object):

    def __init__(self, program_path, arguments, output):
        self.path = program_path
        self.arguments = arguments
        self.output = output

        print(open(self.path + "/lib/misc/banner.txt").read().format(**VERSION))
        self.arguments.configuration

        # Resource instance
        self.resources = Resources(self.path, self.arguments, self.output)

        # Only Validate Modules
        if self.arguments.validation:
            self.ValidateModules()
            sys.exit()

        # Outputs scanning mode
        if self.arguments.modules == "all":
            self.output.InformationalOutput(mode=True)
        else:
            self.output.InformationalOutput(mode=False)

        # Threaded Methods For Faster Creation
        self.HOST_CREATION = threading.Thread(target=self.CreateHostObjects())
        self.APP_CREATION = threading.Thread(target=self.CreateApplicationList())

        #  1) Generate Host Objects
        if self.arguments.hosts:
            self.HOST_CREATION.start()

        # 2) Generate Application List
        if self.arguments.modules:
            self.APP_CREATION.start()

        # Wait for Threads to Finish
        self.HOST_CREATION.join()
        self.APP_CREATION.join()

        # 3) Fingerprint Targets
        if self.arguments.only_fingerprint:
            if host_objects and application_list:
                self.FingerPrintTargets()
            elif host_objects is False:
                self.output.errorOutput(host=True)
        elif bool(host_objects):
            self.FingerPrintTargets()
            application_list.appendHost(host_objects)
        elif bool(host_objects) is False:
            self.output.errorOutput(host=True)
            sys.exit()

        # 4) Move hosts to proper application
        if host_objects and application_list:
            self.application_objects = []
            self.CreateApplicationObjects()

        # 5) Performing Scanning Procedure
        self.ScanProcedure()

        return

    def CreateHostObjects(self):
        """ Creates host Objects Using the Selenium Headless Driver """
        global host_objects

        options = selenium.webdriver.firefox.options.Options()
        options.headless = True
        driver = Firefox(options=options)

        self.output.creationOutput(host=True)

        for host in self.arguments.hosts:
            temp = Host(host,self.arguments, driver=driver)
            if temp.is_alive:
                host_objects.append(temp)
        return

    def CreateApplicationList(self):

        global application_list

        self.output.creationOutput(applicationList=True)
        application_list = ApplicationList(self.arguments, self.resources)

        return

    def CreateApplicationObjects(self):

        self.output.creationOutput(applicationObjects=True)

        for make in application_list.applications:
            for model in application_list.applications[make]:
                if bool(application_list.applications[make][model]):
                    temp_app = Application(make, model, self.resources, application_list.applications[make][model],self.arguments,self.output)
                    temp_app.generateStructure()

                    # Omit Modules if they have no known defaults :: defaulter mode
                    if self.arguments.modules == "all":
                        if bool(temp_app.usernames) is False or bool(temp_app.passwords) is False:
                            self.output.InformationalOutput(omit=temp_app.application_make)
                            continue

                    self.application_objects.append(temp_app)
        return


    def FingerPrintTargets(self):
        self.output.creationOutput(fingerprint=True)
        Fingerprinter(host_objects, application_list.applications,self.output,self.arguments)
        return

    def ValidateModules(self):

        # Validate all modules unless modules are specified
        ApplicationList(self.path, self.arguments, self.resources)

        return

    def ScanProcedure(self):

        self.output.creationOutput(application=True)

        if self.application_objects:
            self.output.creationOutput(startScan=True)
            Authenticator(self.application_objects,self.output,self.arguments).PerformAuthentication()
        else:
            sys.exit()

        return