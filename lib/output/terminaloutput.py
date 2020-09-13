# -*- coding: utf-8 -*-

from lib.misc.colors import Colors
from datetime import datetime


class TerminalOutput(object):

    def __init__(self):
        pass

    def TermOutput(self, host=None, application=None, validUrl=None, username=None,password=None):

        time = datetime.now().strftime("%H:%M:%S")

        # 1 - Print Host Output If Defaulted
        if host:
            if host.defaults:
                    print(Colors.yellow+"{0} :: ".format(time)+Colors.success+"[+] %s%s - Username [ %s ] :: Password [ %s ]"
                          %(host.url,validUrl,username, password))

        # 2 - Print Application Related Information
        if application:
            print(Colors.yellow + "{0} :: ".format(time)+Colors.header+"=> Scanning Application Make [ %s ] :: Model [ %s ] :: Threshold [ %s ]"
                                                   %(application.application_make.upper(),application.application_model, str(application.threshold)))

        return

    def creationOutput(self, host=False, applicationList=False, applicationObjects=False, fingerprint=False,
                       startScan=False, application=False):

        time = datetime.now().strftime("%H:%M:%S")

        if host:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.informational+"=> Creating Host Objects ")

        if applicationList:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.informational+"=> Creating Application List ")

        if fingerprint:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.informational+"=> Fingerprinting Targets ")

        if applicationObjects:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.informational+"=> Creating Application Objects for Scanning ")
        if startScan:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.informational+"=> Starting Scan Procedure ")

        if application:
            print(Colors.yellow + "{0} :: ".format(time) + Colors.informational +"=> Generating Application Structures ")

        return


    def errorOutput(self, host=False, applicationList=False, application=False, fingerprint=False, scan=False
                    ,module=False, file=False, timeout=False, element_issue=False, increase_timing=False):

        time = datetime.now().strftime("%H:%M:%S")

        if host:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.error+"=> Error creating hosts check connectivity")

        if applicationList:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.error+"=> Error creating application list")

        if module:
            print(Colors.yellow + "{0} :: ".format(time) + Colors.error + "[ Invalid Configuration ]"
                  + Colors.end_color + " :: " + module.upper())

        if file:
            print(Colors.yellow + "{0} :: ".format(time) + Colors.error + "[ File not Found  ]"
                  + Colors.end_color + " :: " + file.upper())

        if timeout:
            print(Colors.yellow+"{0} :: ".format(time)+"(!) %s timed out skipping" %timeout.url)

        if element_issue:
            print(Colors.yellow+"{0} :: ".format(time)+"(!) %s Issue Retrieving Page Elements skipping" %element_issue.url)

        if increase_timing:
            print(Colors.yellow+"{0} :: ".format(time)+"(!) Issue Retrieving Page Elements Increasing Page Delay")

        return

    # Informational Related Output
    def InformationalOutput(self, module=None, fingerprint=None, host=None, username=None, password=None, url=None, mode=None, omit=None, model=None):

        time = datetime.now().strftime("%H:%M:%S")

        if module:
                print(Colors.yellow+"{0} :: ".format(time)+Colors.success+"[ Valid Configuration   ]"+Colors.end_color+" :: "+module.upper())

        if fingerprint:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.header+"(!) %s  [ %s ] :: [ %s ]"%(fingerprint.url, fingerprint.application_make.upper(),fingerprint.application_model.upper()))

        if host:
            if username and password:
                print(Colors.yellow+"{0} :: ".format(time)+Colors.error+"[-] %s%s - Username [ %s ] :: Password [ %s ]"%(host, url, username, password))

        if mode is True:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.informational+"=> Defaulter Mode :: Known credentialed modules loaded  ")
        elif mode is False:
            print(Colors.yellow+"{0} :: ".format(time)+Colors.informational+"=> Target Specific Mode")

        if omit:
            print(Colors.yellow+"{0} :: ".format(time)+"(!) Module Omitted no known defaults [ %s ]" %omit.upper())


        if model:
            print(Colors.yellow + "{0} :: ".format(time) + "(!) Model Unknown defaulting to [ %s ] :: [ Configuration: %s ]" %(model[0].upper(),str(model[1])))


        return

