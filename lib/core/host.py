# -*- coding: utf-8 -*-

import requests

class Host(object):

    def __init__(self, url, arguments):

        self.url = url
        self.arguments = arguments
        self.application_make = None
        self.application_model = None
        self.attempts = 0
        self.is_alive = False
        self.scanned = False
        self.defaults = False
        self.valid_defaults = {}
        self.timedOut = False
        self.sample = None

        if self.url.endswith("/"):
            self.url = self.url.rstrip("/")

        if self.scanned is False:
            self.RetrieveSample()


    # Retrieves sample for fingerprinting
    def RetrieveSample(self):

        try:
            response = requests.get(self.url, verify=False, timeout=self.arguments.timeout,proxies=self.arguments.proxy,allow_redirects=True)
            if response.status_code:
                self.is_alive = True
                self.sample = response.text.lower()
        except Exception as error:
            self.is_alive = False

        return
