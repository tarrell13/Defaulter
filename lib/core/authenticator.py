# -*- coding: utf-8 -*-

from lib.core.crafter import Crafter
from lib.output.report import Report
import selenium
import requests
import urllib3
import time
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Authenticator(object):

    def __init__(self, application_objects, output, arguments):
        self.application_objects = application_objects
        self.output = output
        self.arguments = arguments

        if self.arguments.output_file:
            self.reporter = Report(self.arguments.output_file)

        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'identity',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

    def ResetHeaders(self):

        self.headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'identity',
            'Keep-Alive': '300',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

    # Determines if authentication was successful or not
    def CheckAuthentication(self, response, success_tokens, failure_tokens):

        fail = False
        if bool(failure_tokens):
            for failure in failure_tokens:
                try:
                    if isinstance(int(failure),int):
                        if response.status_code == int(failure):
                            fail = True
                        else:
                            fail = False
                            break
                except ValueError:
                    if isinstance(failure,str):
                        if re.search(failure.lower(), str(response.content).lower()):
                            fail = True
                            continue
                        else:
                            fail = False
                            continue
        if fail:
            return False

        for success in success_tokens:
            try:
                if isinstance(int(success), int):
                    if response.status_code == int(success):
                        continue
                    else:
                        return False
            except ValueError:
                if isinstance(success, str):
                    if re.search(success.lower(), str(response.content).lower()):
                        continue
                    else:
                        return False

        return True

    def CheckAuthenticationTest(self, application, page_source=None, current_cookies=None, current_url=None,
                                response=None):
        """ Updated Authentication Check Based on Updated Config """

        authenticated = False

        if application.authentication == "form":
            """ FORM based authentication checks page source and cookies """
            if application.success_tokensv2["COOKIES"]:
                for cookie in application.success_tokensv2["COOKIES"]:
                    if cookie in current_cookies:
                        authenticated = True
                    else:
                        authenticated = False
                        break

            if application.success_tokensv2["URL"]:
                for url in application.success_tokensv2["URL"]:
                    if re.search(url, current_url):
                        authenticated = True
                    else:
                        authenticated = False
                        break

            if application.success_tokensv2["SOURCE"]:
                for phrase in application.success_tokensv2["SOURCE"]:
                    if re.search(phrase, page_source):
                        authenticated = True
                    else:
                        authenticated = False
                        break

            if authenticated:
                return True

        elif application.authentication == "api" or application.authentication == "basic":
            """ API/BASIC Authentication Uses Request Response """
            if authenticated:
                return True

        return False

    def PerformFormAuthenticationTest(self, host, application):
        """ Authenticate account using web page onclick events """
        for post in application.post_uri:
            if self.arguments.stop_host and host.defaults:
                time.sleep(0.5)
                break
            else:
                host.defaults = False

            for username in application.usernames:
                if self.arguments.stop_host and host.defaults:
                    break
                elif self.arguments.stop_url and host.defaults:
                    break
                else:
                    host.defaults = False

                host.attempts = 0

                for password in application.passwords:
                    # Threshold Respect
                    if application.threshold == 0:
                        time.sleep(0.5)
                    elif host.defaults is False and host.attempts < application.threshold:
                        time.sleep(0.5)
                        host.attempts += 1
                    else:
                        break

                    """ Using Selenium Drivers Retrieve, Send and Submit """
                    try:
                        host.driver.get("%s%s" %(host.url, post))

                        if not application.empty_user:
                            user_element = host.driver.find_element_by_name(application.submission["USER"])
                            user_element.send_keys(username)

                        passwd_element = host.driver.find_element_by_name(application.submission["PASS"])
                        passwd_element.send_keys(password)

                        submit_element = host.driver.find_element_by_name(application.submission["SUBMIT"])
                        submit_element.click()

                        source = host.driver.page_source
                        cookies = host.driver.get_cookies()
                        current_url = host.driver.current_url

                        cookie_list = []
                        if cookies:
                            for cookie in cookies:
                                cookie_list.append(cookie["name"])

                    except selenium.common.exceptions.WebDriverException:
                        host.timedOut = True
                        self.output.errorOutput(timeout=host)
                        break

                    if self.CheckAuthenticationTest(application, page_source=source, current_cookies=cookie_list,
                                                    current_url=current_url ):
                    #if self.CheckAuthentication(source, application.success_tokens,application.failure_tokens):
                        host.valid_defaults[post] = {}
                        host.valid_defaults[post][username] = password
                        host.defaults = True
                        host.scanned = True
                        host.attempts = 0
                        self.output.TermOutput(host=host, validUrl=post,
                                               username=username, password=password)
                        if self.arguments.output_file:
                            self.reporter.OutputTXTFile(host=(host.url, post, username, password), default=True)

                    elif self.arguments.verbose or self.arguments.output_file:
                        if self.arguments.verbose:
                            self.output.InformationalOutput(host=host.url, url=post, username=username,
                                                            password=password)
                        if self.arguments.output_file:
                            self.reporter.OutputTXTFile(host=(host.url, post, username, password))

                    # BREAK OUT PASSWORDS
                    if host.defaults:
                        break

                    # BREAK OUT USERNAMES
                if host.timedOut:
                    host.timeOut = False
                    break

    # Reserved for API Authentication Schemes
    def PerformApiAuthentication(self):
        return

    # Reserved for FORM authentication
    def PerformFormAuthentication(self, host, application):

        for post in application.post_uri:
            if self.arguments.stop_host and host.defaults:
                time.sleep(0.5)
                break
            else:
                host.defaults = False

            for username in application.usernames:

                if self.arguments.stop_host and host.defaults:
                    break
                elif self.arguments.stop_url and host.defaults:
                    host.defaults = False
                    break
                else:
                    host.defaults = False

                host.attempts = 0

                for password in application.passwords:
                    # Threshold Respect
                    if application.threshold == 0:
                        time.sleep(0.5)
                    elif host.defaults is False and host.attempts < application.threshold:
                        time.sleep(0.5)
                        host.attempts += 1
                    else:
                        break

                    craft = Crafter(self.arguments, username, password, host, application)

                    try:
                        response = craft.session.post("%s%s" % (host.url, post), verify=False
                                                      , timeout=self.arguments.timeout, data=craft.post_data
                                                      , allow_redirects=application.redirection,
                                                      proxies=self.arguments.proxy)
                    except requests.exceptions.ReadTimeout:
                        host.timedOut = True
                        self.output.errorOutput(timeout=host)
                        break

                    if self.CheckAuthentication(response, application.success_tokens,
                                                application.failure_tokens):
                        host.valid_defaults[post] = {}
                        host.valid_defaults[post][username] = password
                        host.defaults = True
                        host.scanned = True
                        host.attempts = 0
                        self.output.TermOutput(host=host, validUrl=post,
                                               username=username, password=password)
                        if self.arguments.output_file:
                            self.reporter.OutputTXTFile(host=(host.url, post, username, password), default=True)

                    elif self.arguments.verbose or self.arguments.output_file:
                        if self.arguments.verbose:
                            self.output.InformationalOutput(host=host.url, url=post, username=username,
                                                        password=password)
                        if self.arguments.output_file:
                            self.reporter.OutputTXTFile(host=(host.url,post,username,password))


                    # BREAK OUT PASSWORDS
                    if host.defaults:
                        break

                # BREAK OUT USERNAMES
                if host.timedOut:
                    host.timeOut = False
                    break
        return

    # Reserved for Basic Authentication
    def PerformBasicAuthentication(self, host, application):

        for get in application.get_uri:

            if self.arguments.stop_host and host.defaults:
                time.sleep(0.5)
                break
            else:
                host.defaults = False

            for username in application.usernames:

                if self.arguments.stop_host and host.defaults:
                    break
                elif self.arguments.stop_url and host.defaults:
                    host.defaults = False
                    break
                else:
                    host.defaults = False

                host.attempts = 0

                for password in application.passwords:

                    if application.threshold == 0:
                        time.sleep(0.5)
                    elif host.defaults is False and host.attempts < application.threshold:
                        time.sleep(0.5)
                        host.attempts += 1
                    else:
                        break

                    craft = Crafter(self.arguments, username, password, host, application)

                    try:
                        response = requests.get("%s%s" % (host.url, get), verify=False,
                                                headers=craft.headers, allow_redirects=application.redirection,
                                                timeout=self.arguments.timeout, proxies=self.arguments.proxy)

                    except requests.exceptions.ReadTimeout:
                        host.timedOut = True
                        self.output.errorOutput(timeout=host)
                        break

                    if self.CheckAuthentication(response, application.success_tokens, application.failure_tokens):
                        host.valid_defaults[get] = {}
                        host.valid_defaults[get][username] = password
                        host.defaults = True
                        host.scanned = True
                        host.attempts = 0
                        self.output.TermOutput(host=host, validUrl=get,
                                               username=username, password=password)
                    elif self.arguments.verbose:
                        self.output.InformationalOutput(host=host.url, url=get, username=username,
                                                        password=password)

                    self.ResetHeaders()

                    if host.defaults:
                        break

                if host.timedOut:
                    host.timedOut = False
                    break

        return

    def PerformAuthentication(self):

        for application in self.application_objects:
            self.output.TermOutput(application=application)
            if self.arguments.output_file:
                self.reporter.OutputTXTFile(application=(application.application_make,application.application_model))

            time.sleep(1)

            for host in application.host_list:
                if application.authentication.lower() == "form" or application.authentication.lower() == "api":
                    self.PerformFormAuthenticationTest(host,application)
                elif application.authentication.lower() == "basic":
                    self.PerformBasicAuthentication(host,application)

                host.scanned = True
        return