__author__ = 'Kedar Subramanya'
from uuid import getnode as get_mac
import json
from pprint import pprint

class ConfigService(object):
    """ this class loads the settings from config file and also reads from the deployed machine
    for things like Mac id to uniquely identify the device
    """
    def __init__(self):
        self.Email = ""
        self.AccountName = ""
        self.AccountKey = ""
        self.StorageType = ""
        self.DeviceId = ""
        self.DeviceDescription = ""
        self.UserName = ""
        self.Email = ""
        self.MacAddress = ""

    def byteify(self, input):
        if isinstance(input, dict):
            return {self.byteify(key):self.byteify(value) for key,value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def loadConfig(self):
        with open("settings.json") as json_file:
            json_data = json.load(json_file)
        print(json_data)

        json_file.close()

        json_data = self.byteify(json_data)

        self.Email = json_data["email"]
        self.AccountName = json_data["accountname"]
        self.AccountKey = json_data["accountkey"]
        self.StorageType = json_data["storagetype"]
        self.DeviceId = json_data["deviceid"]
        self.DeviceDescription = json_data["devicedescription"]
        self.UserName = json_data["username"]
        self.Email = json_data["email"]
        self.MacAddress = self.getMacAddress()

    def getMacAddress(self):
        return get_mac()

    def whatsInside(self):
        print(self.Email)
        print(self.MacAddress)
        print(self.AccountName)
        print(self.AccountKey)
        print(self.StorageType)


