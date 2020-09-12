# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

class Host(object):

    def __init__(self, url, arguments, driver=None):

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
        self.driver = driver

        if self.url.endswith("/"):
            self.url = self.url.rstrip("/")

        if self.scanned is False:
            self.RetrieveSampleTest()

    ''' Retrieves sample for fingerprinting '''
    def RetrieveSample(self):
        try:
            response = requests.get(self.url, verify=False, timeout=self.arguments.timeout,proxies=self.arguments.proxy,allow_redirects=True)
            if response.status_code:
                self.is_alive = True
                self.sample = response.text.lower()
        except Exception as error:
            self.is_alive = False

    def meta_refresh(self, content):
        """ Determines if page root has a redirect to true page """
        soup = BeautifulSoup(content.lower(), features="lxml")

        result = soup.find("meta", attrs={"http-equiv": "refresh"})
        if result:
            wait, text = result["content"].split(";")
            if text.strip().lower().startswith("url="):
                self.url = text[5:]
                return True
        return False

    def RetrieveSampleTest(self):
        """ Retrieve Method Utilizing Selenium Request """
        try:
            response = self.driver.request("GET", self.url, verify=False, timeout=self.arguments.timeout,
                                           proxies=self.arguments.proxy, allow_redirects=True)
            if response.status_code:
                if self.meta_refresh(response.content.decode()):
                    response = self.driver.request("GET", self.url, verify=False, timeout=self.arguments.timeout,
                                                   proxies=self.arguments.proxy, allow_redirects=True)
                    if response.status_code:
                        self.is_alive = True
                        self.sample = response.text.lower()
                else:
                    self.is_alive = True
                    self.sample = response.text.lower()
        except Exception as error:
            self.is_alive = False

