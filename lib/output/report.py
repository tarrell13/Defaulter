# -*- coding: utf-8 -*-

import os

class Report(object):

    def __init__(self, filename):
        self.filename = filename
        open(self.filename,"w").close()

    # Output information to text file
    def OutputTXTFile(self, application=None, host=None, default=False):

        if application:
            with open(self.filename,"a") as myFile:
                myFile.write("[ Application [ %s ] :: [ %s ] ]\n\n" %(application[0],application[1]))
                myFile.close()

        if host:
            with open(self.filename,"a") as myFile:
                if default:
                    myFile.write("[ SUCCESS ] %s%s => Username [ %s ] : Password [ %s ]\n"
                                 %(host[0],host[1],host[2],host[3]))
                else:
                    myFile.write("[ FAIL ] %s%s => Username [ %s ] : Password [ %s ]\n"
                                 % (host[0], host[1],host[2],host[3]))
        return


    def OutputHTMLFile(self):
        pass

