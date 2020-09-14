# -*- coding: utf-8 -*-


class Application(object):

    def __init__(self, make, model, resources, host_list, arguments,output):

        self.arguments = arguments
        self.output = output
        self.DATA = resources.QueryApplicationModule(make)
        self.model_struct = resources.QueryApplicationModelStruct(model)
        self.application_make = make
        self.application_model = model
        self.get_uri = None
        self.post_uri = None
        self.success_tokens = None
        self.failure_tokens = None
        self.token_uri = None
        self.authentication = None
        self.usernames = None
        self.passwords = None
        self.threshold = 0
        self.parameters = None
        self.cookies = None
        self.redirection = None
        self.submission = None
        self.empty_user = False

        """ Success V2 Test """
        self.success_tokensv2 = None

        """ For Event Based Submission """
        self.element_by_name = False
        self.element_by_id = False

        # Initialize host list
        self.host_list = host_list

    def CheckEmptyUser(self):
        """ Checks If the Application Utilizes Both Username and/or Password """
        if self.passwords and not self.usernames or self.usernames[0] == "NONE":
            self.empty_user = True

    @property
    def information(self):
        print("Application Make [ %s ] :: Model [ %s ]" %(self.application_make,self.application_model))

        for host in self.host_list:
            print("- " + host.url)

    @property
    def informationStruct(self):

        print("[ * ] Scanning Structure [ * ]")
        print("="*len("[ * ] Scanning Structure [ * ]"))
        print("[!] Application Make: %s" %self.application_make)
        print("[!] Application Model: %s" %self.application_model)
        print("[!] GET URI: " + str(self.get_uri))
        print("[!] POST URI: " + str(self.post_uri))
        print("[!] Success Tokens: "+ str(self.success_tokens))
        print("[!] Failure Tokens: "+ str(self.failure_tokens))
        print("[!] Authentication: " + self.authentication)
        print("[!] Usernames: "+ str(self.usernames))
        print("[!] Passwords: "+ str(self.passwords))
        print("[!] Guess Attempts: "+ str(self.threshold))
        print("[!] Cookies: "+str(self.cookies))
        print("[!] Parameters: "+ str(self.parameters))

    # Appends host to application host list array ?? May not need this functionality
    def appendHost(self, host):
        self.host_list.append(host)

    # Generates the application structure
    def generateStructure(self):

        if self.arguments.custom:
            self.authentication = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["AUTHENTICATION"]
            self.get_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["URI"]["GET"]
            self.post_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["URI"]["POST"]
            self.success_tokens = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["SUCCESS_TOKENS"]
            self.failure_tokens = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["FAILURE_TOKENS"]
            self.parameters = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["PARAMETERS"]
            self.threshold = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["THRESHOLD"]
            self.usernames = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["USERNAMES"]
            self.passwords = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["PASSWORDS"]
            self.cookies = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["COOKIES"]
            self.redirection = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["REDIRECTION"]
            self.token_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["TOKEN_URI"]
            self.success_tokensv2 = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["SUCCESSV2"]
            self.submission = self.DATA["STRUCTURE"]["CONFIGURATION"][0]["SUBMISSION"]

        elif self.arguments.mod_config != "defaults":
            for make,config in self.arguments.mod_config.items():
                if make.lower() == self.application_make.lower():
                    config = int(config)
                    self.authentication = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["AUTHENTICATION"]
                    self.get_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["URI"]["GET"]
                    self.post_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["URI"]["POST"]
                    self.success_tokens = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["SUCCESS_TOKENS"]
                    self.failure_tokens = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["FAILURE_TOKENS"]
                    self.parameters = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["PARAMETERS"]
                    self.threshold = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["THRESHOLD"]
                    self.usernames = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["USERNAMES"]
                    self.passwords = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["PASSWORDS"]
                    self.cookies = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["COOKIES"]
                    self.redirection = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["REDIRECTION"]
                    self.token_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["TOKEN_URI"]
                    self.success_tokensv2 = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["SUCCESSV2"]
                    self.submission = self.DATA["STRUCTURE"]["CONFIGURATION"][config]["SUBMISSION"]

                    #break

        elif self.application_model is not "unknown":
            self.get_uri = self.model_struct["URI"]["GET"]
            self.post_uri = self.model_struct["URI"]["POST"]
            self.success_tokens = self.model_struct["SUCCESS_TOKENS"]
            self.failure_tokens = self.model_struct["FAILURE_TOKENS"]
            self.threshold = self.model_struct["THRESHOLD"]
            self.parameters = self.model_struct["PARAMETERS"]
            self.usernames = self.model_struct["USERNAMES"]
            self.passwords = self.model_struct["PASSWORDS"]
            self.cookies = self.model_struct["COOKIES"]
            self.authentication = self.model_struct["AUTHENTICATION"]
            self.token_uri = self.model_struct["TOKEN_URI"]
            self.redirection = self.model_struct["REDIRECTION"]
            self.success_tokensv2 = self.model_struct["SUCCESSV2"]
            self.submission = self.model_struct["SUBMISSION"]

        elif self.application_model is "unknown":

            index = None
            max = 0

            for i in range(len(self.DATA["STRUCTURE"]["CONFIGURATION"])):

                if index is None:
                    index = i
                    max = len(self.DATA["STRUCTURE"]["CONFIGURATION"][index]["MODELS"])
                    continue

                elif max < len(self.DATA["STRUCTURE"]["CONFIGURATION"][i]["MODELS"]):
                    index = i
                    max = len(self.DATA["STRUCTURE"]["CONFIGURATION"][i]["MODELS"])

            self.authentication = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["AUTHENTICATION"]
            self.get_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["URI"]["GET"]
            self.post_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["URI"]["POST"]
            self.success_tokens = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["SUCCESS_TOKENS"]
            self.failure_tokens = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["FAILURE_TOKENS"]
            self.parameters = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["PARAMETERS"]
            self.threshold = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["THRESHOLD"]
            self.usernames = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["USERNAMES"]
            self.passwords = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["PASSWORDS"]
            self.cookies = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["COOKIES"]
            self.redirection = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["REDIRECTION"]
            self.token_uri = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["TOKEN_URI"]
            self.success_tokensv2 = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["SUCCESSV2"]
            self.submission = self.DATA["STRUCTURE"]["CONFIGURATION"][index]["SUBMISSION"]

        self.ParseArgumentsIntoStructure()
        self.CheckEmptyUser()

    def ParseArgumentsIntoStructure(self):

        # Parse cookie value from arguments to configuration if defaulted
        if self.arguments.cookies == "defaults":
            if self.cookies.lower() == "true":
                self.cookies = True
            else:
                self.cookies = False
        elif self.arguments.cookies == "true":
            self.cookies = True
        elif self.arguments.cookies == "false":
            self.cookies = False

        # Parse usernames
        if self.arguments.usernames == "defaults":
            pass
        else:
            self.usernames = self.arguments.usernames

        # Parse passwords
        if self.arguments.passwords == "defaults":
            pass
        else:
            self.passwords = self.arguments.passwords

        # Parse potential threshold value
        try:
            if self.arguments.disrespect:
                self.threshold = 0
            elif bool(type(int(self.threshold)) is int) and self.arguments.disrespect is False:
                self.threshold = int(self.threshold)
        except ValueError:
            self.threshold = 0

        # Parse success tokens
        if self.arguments.success == "defaults":
            pass
        else:
            self.success_tokens = self.arguments.success

        # Parse failure tokens
        if self.arguments.failure == "defaults":
            pass
        else:
            self.failure_tokens = self.arguments.failure

        # Parse redirection values
        if self.arguments.redirection == "defaults":
            if self.redirection.lower() == "true":
                self.redirection = True
            else:
                self.redirection = False
        elif self.arguments.redirection is True:
            self.redirection = True
        elif self.arguments.redirection is False:
            self.redirection = False

        # Parse TOKEN URI
        if self.arguments.token_uri == "defaults":
            pass
        else:
            self.token_uri = self.arguments.token_uri

        # Parse GET URL
        if self.arguments.get_url == "defaults":
            pass
        else:
            self.get_uri = self.arguments.get_url

        # Parse POST URL
        if self.arguments.post_url == "defaults":
            pass
        else:
            self.post_uri = self.arguments.post_url

        if self.arguments.auth_type == "defaults":
            pass
        elif self.arguments.auth_type.lower() in [ "basic", "form", "api"]:
            self.authentication = self.arguments.auth_type.lower()

        if self.arguments.user_param == "defaults":
            pass
        else:
            self.parameters["USER_PARAMETER"] = self.arguments.user_param

        if self.arguments.pass_param == "defaults":
            pass
        else:
            self.parameters["PASS_PARAMETER"] = self.arguments.pass_param
