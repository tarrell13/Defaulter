# -*- coding: utf-8 -*-

from optparse import OptionParser, OptionGroup
import sys
import re
import os

class Arguments(object):


    def __init__(self, path):

        self.path = path

        options = self.ParseOptions()
        self.copy_options = options

        if options.validation is False:
            # Configure required options
            if options.input is not None:
                self.hosts = []
                if os.path.exists(options.input):
                    for line in open(options.input,"r").readlines():
                        self.hosts.append(line.rstrip())
                elif re.search(",", options.input):
                    temp_host = options.input.split(",")
                    for host in temp_host:
                        if host.startswith("http://") or host.startswith("https://"):
                            self.hosts.append(host)
                elif options.input.startswith("http://") or options.input.startswith("https://"):
                    self.hosts = []
                    self.hosts.append(options.input)
                else:
                    print("[!] Error reading input. Enter URL or file containing URLs")
                    sys.exit()
            else:
                print("[!] Error reading input. Enter URL or file containing URLs")
                sys.exit()

        #############################
        # Configure Optionals Overall
        #############################
        if options.verbose:
            self.verbose = True
        else:
            self.verbose = False

        # Timeout settings
        if options.timeout:
            self.timeout = options.timeout
        else:
            self.timeout = 3

        # Fingerprinting settings
        if options.fingerprint:
            self.only_fingerprint = True
        else:
            self.only_fingerprint = False

        if options.users is not None:
            self.usernames = []
            if os.path.exists(options.users):
                for line in open(options.users,"r").readlines():
                    self.usernames.append(line.rstrip())
            elif re.search(",", options.users):
                self.usernames = options.users.split(",")
            else:
                self.usernames.append(options.users)
        else:
            self.usernames = "defaults"

        if options.passwords is not  None:
            self.passwords = []
            if os.path.exists(options.passwords):
                for line in open(options.passwords,"r").readlines():
                    self.passwords.append(line.rstrip())
            elif re.search(",", options.passwords):
                self.passwords = options.passwords.split(",")
            else:
                self.passwords.append(options.passwords)
        else:
            self.passwords = "defaults"

        # Disrespect settings
        if options.disrespect:
            self.disrespect = True
        else:
            self.disrespect = False

        if options.validation:
            self.validation = True
        else:
            self.validation = False

        # Stop Scanning Host on success
        if options.stop_host:
            self.stop_host = True
        else:
            self.stop_host = False

        # Stop Scanning URL on success
        if options.stop_url:
            self.stop_url = True
        else:
            self.stop_url = False

        # PROXY Settings
        if options.proxy:
            if options.proxy.startswith("http:") or options.proxy.startswith("https:"):
                self.proxy = {}
                components = options.proxy.split(":")
                if len(components) != 3:
                    print("(!) Proxy settings need to be in form http:localhost:8080 or https:localhost:8008")
                    sys.exit()
                else:
                    self.proxy[components[0]] = components[0] + "://" + components[1] + ":" + components[2]
            else:
                print("(!) Proxy settings need to be in form http:localhost:8080 or https:localhost:8008")
                sys.exit()

        else:
            self.proxy = None


        # Output Settings
        if options.output_txt:
            self.output_file = options.output_txt
        else:
            self.output_file = False

        ##############################################
        # Configure Options for Targeted Scanning Mode
        ##############################################

        # Only Modules
        if options.modules is not None or options.custom:

            if options.custom and self.ParseCustomAuthMode(options):
                self.custom = True
                self.auth_type = options.auth_type.lower()
                options.modules = "custom"
            elif options.custom and self.ParseCustomAuthMode(options) is False:
                sys.exit()
            else:
                self.custom = False

            self.modules = []
            if os.path.exists(options.modules):
                for line in open(options.modules,"r").readlines():
                    self.modules.append(line.rstrip())
            elif re.search(",", options.modules):
                self.modules = options.modules.split(",")
            else:
                self.modules.append(options.modules)

            if options.success and self.modules != "all":
                self.success= []
                if re.search(",", options.success):
                    self.success = options.success.split(",")
                else:
                    self.success.append(options.success)
            elif options.success and self.modules == "all":
                print("[!] Custom success tokens can only be used with --only-module")
                sys.exit()
            else:
                self.success = "defaults"

            if options.failure and self.modules != "all":
                self.failure = []
                if re.search(",", options.failure):
                    self.failure = options.failure.split(",")
                else:
                    self.failure.append(options.failure)
            elif options.failure and self.modules == "all":
                print("[!] Custom failure tokens can only be used with --only-module")
                sys.exit()
            else:
                self.failure = "defaults"

            # REDIRECTION settings
            try:
                if options.redirection.lower() == "true":
                    self.redirection = True
                elif options.redirection.lower() == "false":
                    self.redirection = False
                else:
                    if options.custom:
                        self.redirection = False
                    else:
                        self.redirection = "defaults"
            except AttributeError:
                if options.custom:
                    self.redirection = False
                else:
                    self.redirection = "defaults"

            if options.token:
                self.token_uri = options.token
            else:
                self.token_uri = "defaults"

            if options.post_url:
                self.post_url = []
                if re.search(",",options.post_url):
                    self.post_url = options.post_url.split(",")
                else:
                    self.post_url.append(options.post_url)
            else:
                self.post_url = "defaults"

            if options.get_url:
                self.get_url = []
                if re.search(",",options.get_url):
                    self.get_url = options.get_url.split(",")
                else:
                    self.get_url.append(options.get_url)
            else:
                self.get_url = "defaults"

            if options.cookies:
                self.cookies = True
            else:
                self.cookies = False

            if options.user_param:
                self.user_param = options.user_param
            else:
                self.user_param = "defaults"

            if options.auth_type:
                if options.auth_type.lower() in ["form","api","basic"]:
                    self.auth_type = options.auth_type.lower()
            else:
                self.auth_type = "defaults"

            if options.pass_param:
                self.pass_param = options.pass_param
            else:
                self.pass_param = "defaults"

            if options.mod_config:
                temp_config = {}
                self.mod_config = {}
                if re.search(",", options.mod_config):
                    temp = options.mod_config.split(",")
                    for item in temp:
                        if re.search(":", item):
                            if self.CheckModConfigKeyValue(item.split(":")[0],item.split(":")[1]):
                                temp_config[item.split(":")[0]] = item.split(":")[1]
                elif re.search(":", options.mod_config):
                    if self.CheckModConfigKeyValue(options.mod_config.split(":")[0], options.mod_config.split(":")[1]):
                        temp_config[options.mod_config.split(":")[0]] = options.mod_config.split(":")[1]

                if temp_config:
                    for make,config in temp_config.items():
                        if make in self.modules:
                            self.mod_config[make] = config
            else:
                self.mod_config = "defaults"
        else:
            self.modules = "all"
            self.success = "defaults"
            self.failure = "defaults"
            self.redirection = "defaults"
            self.token_uri = "defaults"
            self.post_url = "defaults"
            self.get_url = "defaults"
            self.mod_config = "defaults"
            self.cookies = "defaults"
            self.auth_type = "defaults"
            self.user_param = "defaults"
            self.pass_param = "defaults"
            self.custom = False


    def CheckModConfigKeyValue(self, make, config):

        try:
            if isinstance(make,str) and isinstance(int(config),int):
                return True
        except ValueError:
            print("(!) Parsing Error Mod Config Mode :: Expected Input 'wordpress:0'")
            sys.exit()

        return False

    @property
    def configuration(self):
        print("(!) Current Configuration")
        print("(!) Target(s): %s" %self.copy_options.input)
        print("(!) Username(s): %s" %self.copy_options.users)
        print("(!) Password(s): %s" %self.copy_options.passwords)
        print("(!) Timeout Value: %s" %str(self.timeout))
        print("(!) Stop against host on success:  %s" %str(self.stop_host))
        print("(!) Stop against URL on success: %s" %str(self.stop_url))
        print("(!) Disrespect: %s" %self.copy_options.disrespect)
        print("(!) Success Tokens: "+ str(self.success))
        print("(!) Failure Tokens: "+ str(self.failure))
        print("(!) Proxy Settings: %s" %str(self.proxy))
        print("(!) Redirection Setting: %s" %str(self.redirection))
        print("(!) Cookies Enabled: %s" %str(self.cookies))
        print("(!) Custom Token URI: %s" %self.token_uri)
        print("(!) Custom GET URL: %s" %self.get_url)
        print("(!) Custom POST URL: %s" %self.post_url)
        print("(!) Module Config: "+str(self.mod_config))
        print("(!) Only Modules: %s\n\n" %self.modules)

    # IF Only Module is set to custom properly check fields
    def ParseCustomAuthMode(self, options):

        if options.auth_type:
            auth_type = options.auth_type.lower()
        else:
            print("(!) Authentication Type is needed [ Basic / Form ]")
            return False

        if auth_type in [ "basic", "form", "api" ]:
            if auth_type == "form":

                if options.post_url is None:
                    print("(!) POST URL needed for authentication method")
                    return False

                if options.cookies:
                    if options.token is None:
                        print("(!) Token URI needed for session establishment")
                        return False
                else:
                    return False

                if options.user_param is None:
                    print("(!) Username parameter name must be specified")
                    return False

                if options.pass_param is None:
                    print("(!) Password parameter name must be specified")
                    return

            elif auth_type == "basic":

                if options.get_url is None:
                    print("(!) GET URL is needed for basic authentication")
                    return False

            if options.success is None and options.failure is None:
                print("(!) At least one valid success or failure token needed")
                return False

        return True


    def ParseOptions(self):

        usage = 'Usage: ./defaulter [-i|--input] target [options]'
        parser = OptionParser(usage)

        # Required options
        required = OptionGroup(parser, 'Required')
        required.add_option('-i', '--input', help='URL target or File containing URLs', action='store', type='string',
                                dest='input', default=None)

        # Informational options
        informational = OptionGroup(parser, 'Informational options')
        informational.add_option('-v', '--verbose', help="Outputs more information", action='store_true',
                                 dest="verbose", default=False)
        informational.add_option("--validation", help="Validates module configuration [ ALL by default] also works with targeted modules", action="store_true",
                                 dest="validation", default=False)

        # Output Options
        output = OptionGroup(parser, "Output Options")
        output.add_option("--output-txt", help="Outputs results to TXT", action="store",type="string", dest="output_txt")

        # Scanning options
        scanning = OptionGroup(parser, "Scanning related options")
        scanning.add_option("--only-fingerprint", help="Scanning will only fingerprint targets", action="store_true",
                            dest="fingerprint", default=False)
        scanning.add_option("-u", "--users", help="List of usernames or comma separated", action="store", type="string",
                            default=None,dest="users")
        scanning.add_option("-p","--passwords",help="List of passwords or comma separated", action="store", type="string",
                            default=None,dest="passwords")
        scanning.add_option("--disrespect", help="Disregard modules threshold value", action="store_true",
                            dest="disrespect", default=False)
        scanning.add_option("--only-modules", help="Activates particular modules, default will load anything in modules directory"
                            ,action="store",type="string", dest="modules", default=None)
        scanning.add_option("-t","--timeout",help="Set timeout :: default [3]", type="int", action="store", default=3,
                            dest="timeout")
        scanning.add_option("--stop-host", help="Stop scanning host on first successful user hit", action="store_true",
                            dest="stop_host",default=False)
        scanning.add_option("--stop-url",help="Stop scanning URL on first successful hit", action="store_true"
                            ,dest="stop_url",default=False)

        scanning.add_option("--proxy", help="Proxy settings in form 'http:localhost:8080'", type="string",action="store",dest="proxy")


        # Custom Scan Options
        custom = OptionGroup(parser, "Custom Scanning [ --only-modules or --custom] options")
        custom.add_option("--success", help="Define custom success tokens with --only-module", type="string",action="store", dest="success")
        custom.add_option("--failure", help="Define custom failure tokens with --only-module", type="string", action="store", dest="failure")
        custom.add_option("--redirection", help="Instructs authentication to follow redirects [True/False] otherwise follows modules settings", type="string", action="store", dest="redirection")
        custom.add_option("--token-uri", help="Custom URI to retrieve hidden inputs used for authentication", type="string", action="store",dest="token")
        custom.add_option("--post-url", help="Custom post url for application", type="string",action="store",dest="post_url")
        custom.add_option("--get-url", help="Custom get url for application", type="string",action="store",dest="get_url")
        custom.add_option("--mod-config", help="Force authentication to utilize particular config regardless of fingerprint. Inputting 'wordpress:0' will use the first configuration in wordpress\
                          can be comma separated",action="store",type="string",dest="mod_config")
        custom.add_option("--auth", help="Authentication Type used [ Basic / Form / Api ]", action="store", type="string", dest="auth_type")
        custom.add_option("--cookies", help="Determines if a session needs to be established first", action="store_true", dest="cookies")
        custom.add_option("--custom", help="Allows custom authentication specification",action="store_true",dest="custom")
        custom.add_option("--user-param",help="Username parameter for login to application",type="string",action="store",dest="user_param")
        custom.add_option("--pass-param",help="Password parameter for login to application",type="string",action="store",dest="pass_param")

        parser.add_option_group(required)
        parser.add_option_group(informational)
        parser.add_option_group(output)
        parser.add_option_group(scanning)
        parser.add_option_group(custom)

        options, arguments = parser.parse_args()

        return options