""" NOT IMPLEMENTED YET STILL BUIDLING """

class Vendor(object):
    """ Vendor Schema """
    def __init__(self, vendor_name, data):
        self.vendor_name = vendor_name
        self.vendor_configs = []
        self.vendor_prints = None
        self.vendor_users = None
        self.vendor_passwords = None
        self.hosts = []

        if data["FINGERPRINTS"]:
            self.vendor_prints = Finger(data["FINGERPRINTS"])

        if data["DEFAULT_USERS"]:
            self.vendor_users = data["DEFAULT_USERS"]

        if data["DEFAULT_PASSWORDS"]:
            self.vendor_passwords = data["DEFAULT_PASSWORDS"]

        if data["CONFIGURATIONS"]:
            for configuration in data["CONFIGURATIONS"]:
                self.vendor_configs.append(Configuration(configuration))

    @property
    def total_configurations(self):
        return len(self.vendor_configs)

    @property
    def total_models(self):
        temp_models = []
        for configuration in self.vendor_configs:
            for model in configuration.models:
                if model.lower() not in temp_models:
                    temp_models.append(model.lower())
        return len(temp_models)

    @property
    def defaulted_vendor(self):
        if self.vendor_users and self.vendor_passwords:
            return True
        else:
            return False


class Configuration(object):
    """ Vendor Configuration Schema """
    def __init__(self, configuration):
        self.authentication = None
        self.models = []

        """ URI Properties """
        self.uri_get = []
        self.uri_post = []

        """ Submission Properties """
        self.user_element_class = None
        self.user_element_name = None
        self.user_element_id = None

        self.password_element_class = None
        self.password_element_name = None
        self.password_element_id = None

        self.submit_element_class = None
        self.submit_element_name = None
        self.submit_element_id = None

        """ SUCCESS PROPERTIES  """
        self.success_status_code = None
        self.success_cookies = []
        self.success_uri = None
        self.success_page_source = []

        self.generate(configuration)

    def generate(self, configuration):
        """ Initializes Properties """

        if configuration["AUTHENTICATION"].upper() in ["FORM", "API", "BASIC"]:
            self.authentication = configuration["AUTHENTICATION"].upper()

        if configuration["MODELS"]:
            self.models = configuration["MODELS"]

        if configuration["URI"]:
            if configuration["URI"]["GET"]:
                self.uri_get = configuration["URI"]["GET"]

            if configuration["URI"]["POST"]:
                self.uri_post = configuration["URI"]["POST"]

        if configuration["SUBMISSION"]:
            if configuration["SUBMISSION"]["USER"]:
                if configuration["SUBMISSION"]["USER"]["CLASS"]:
                    self.user_element_class = configuration["SUBMISSION"]["USER"]["CLASS"]

                if configuration["SUBMISSION"]["USER"]["NAME"]:
                    self.user_element_name = configuration["CONFIGURATION"]["USER"]["NAME"]

                if configuration["SUBMISSION"]["USER"]["ID"]:
                    self.user_element_id = configuration["SUBMISSION"]["USER"]["ID"]

            if configuration["SUBMISSION"]["PASS"]:
                if configuration["SUBMISSION"]["PASS"]["CLASS"]:
                    self.password_element_class = configuration["SUBMISSION"]["PASS"]["CLASS"]

                if configuration["SUBMISSION"]["PASS"]["NAME"]:
                    self.password_element_name = configuration["SUBMISSION"]["PASS"]["NAME"]

                if configuration["SUBMISSION"]["PASS"]["ID"]:
                    self.password_element_id = configuration["SUBMISSION"]["PASS"]["ID"]

            if configuration["SUBMISSION"]["SUBMIT"]:
                if configuration["SUBMISSION"]["SUBMIT"]["CLASS"]:
                    self.submit_element_class = configuration["SUBMISSION"]["SUBMIT"]["CLASS"]

                if configuration["SUBMISSION"]["SUBMIT"]["NAME"]:
                    self.submit_element_name = configuration["SUBMISSION"]["SUBMIT"]["NAME"]

                if configuration["SUBMISSION"]["SUBMIT"]["ID"]:
                    self.submit_element_id = configuration["SUBMISSION"]["SUBMIT"]["ID"]

        if configuration["SUCCESS"]:
            if configuration["SUCCESS"]["STATUS_CODE"]:
                self.success_status_code = configuration["SUCCESS"]["STATUS_CODE"]

            if configuration["SUCCESS"]["COOKIES"]:
                self.success_cookies = configuration["SUCCESS"]["COOKIES"]

            if configuration["SUCCESS"]["URI"]:
                self.success_uri = configuration["SUCCESS"]["URI"]

            if configuration["SUCCESS"]["PAGE_SOURCE"]:
                self.success_page_source = configuration["SUCCESS"]["PAGE_SOURCE"]


class Finger(object):
    """ Vendor FingerPrint Schema """
    def __init__(self, prints):
        self.cookies = None
        self.page_source = None
        self.generate(prints)

    def generate(self, prints):
        """ Generates Prints """
        if prints["HEADERS"]["COOKIES"]:
            self.cookies = prints["HEADERS"]["COOKIES"]

        if prints["HEADERS"]["PAGE_SOURCE"]:
            self.page_source = prints["HEADERS"]["PAGE_SOURCE"]