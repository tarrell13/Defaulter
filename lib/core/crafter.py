# -*- coding: utf-8 -*-

import requests
import base64
import bs4
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Crafter(object):

    def __init__(self, arguments, username, password, url, application):
        self.application = application
        self.arguments = arguments
        self.username = username
        self.password = password
        self.url = url

        # Data will populate depending on craft
        self.post_data = {}
        self.cookie_data = {}
        self.session = None
        self.response = None

        self.headers = {

            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'gzip, deflate',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

        # If attempt requires session
        if self.application.cookies or self.application.token_uri:
            self.RetrieveSession()

        if self.application.authentication == "basic":
            self.HttpBasicAuthentication()
        elif self.application.authentication.lower() == "form":
            self.FormBasedAuthentication()
            self.post_data[self.application.parameters["USER_PARAMETER"]] = username
            self.post_data[self.application.parameters["PASS_PARAMETER"]] = password
        elif self.application.authentication.lower() == "api":
            self.session = requests
            self.FormBasedAuthentication()
            self.post_data[self.application.parameters["USER_PARAMETER"]] = username
            self.post_data[self.application.parameters["PASS_PARAMETER"]] = password

        return

    # HTTP BASIC AUTHENTICATION
    def HttpBasicAuthentication(self):
        credentials = base64.b64encode(b"%s:%s" % (self.username.encode(), self.password.encode())).decode()
        self.headers["Authorization"] = "Basic %s" % credentials

    # FORM BASED AUTHENTICATION
    def FormBasedAuthentication(self):

        if self.application.parameters["STATIC"]:
            self.StaticBuild()

        if self.application.parameters["DYNAMIC"] or self.application.token_uri:
            self.DynamicBuild()

        return

    # Retrieve Dynamic Values and adds to Data
    def DynamicBuild(self):

        self.RetrieveHiddenInputs()

        soup = bs4.BeautifulSoup(self.response.text, "html.parser")

        for param in self.application.parameters["DYNAMIC"]:
            if bool(soup.find("input", {"name": "%s" % param})):
                self.post_data[param] = soup.find("input", {"name": "%s" % param}).get("value")

    # Adds Static Parameters to Data
    def StaticBuild(self):

        for param, value in self.application.parameters["STATIC"].items():
            self.post_data[param] = value

    # Prototype Cookie function
    def RetrieveSession(self):

        self.session = requests.Session()
        self.response = self.session.get("%s%s" % (self.url, self.application.token_uri), verify=False,
                                         timeout=self.arguments.timeout,proxies=self.arguments.proxy)

    # Retrieve Hidden input Values that may be dynamic
    def RetrieveHiddenInputs(self):

        if self.session is None:
            self.session = requests.Session()
            self.response = self.session.get("%s%s" % (self.url, self.application.token_uri), verify=False,
                                             timeout=self.arguments.timeout,proxies=self.arguments.proxy)

        soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        hidden_tags = soup.find_all("input", type="hidden")
        for tag in hidden_tags:
            self.application.parameters["DYNAMIC"].append(tag.get("name"))