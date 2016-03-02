from .call import Call
from .sms import SMS
from .exception import *
import requests
from requests_throttler_exotel import BaseThrottler

class Exotel(object):
    def __init__(self):
        self.sid = None
        self.token = None

        #Init the throttler that will be used for all the SMS & Call objects
        self.throttler = BaseThrottler(name='exotel-throttler',\
         reqs_over_time=(200,60))

        #Start the throttler immediately
        self.throttler.start()

        self.api_base_url = None

    def call(self):

        #Check if SID & Token are present or not. Raise error if not
        if(not self.sid and not self.token):
            raise AccountUninitializedError()

        #Set base URL for API calls. Set now since SID is required
        self.api_base_url = 'https://twilix.exotel.in/v1/Accounts/'+ self.sid

        return Call(self)

    def sms(self):

        #Check if SID & Token are present or not. Raise error if not
        if(not self.sid and not self.token):
            raise AccountUninitializedError()

        #Set base URL for API calls. Set now since SID is required
        self.api_base_url = 'https://twilix.exotel.in/v1/Accounts/'+ self.sid

        return SMS(self)

    def bye(self):

        #Shutdown the throttler
        self.throttler.shutdown()
