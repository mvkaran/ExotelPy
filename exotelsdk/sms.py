from .exception import *
import requests
import base64
import json
import copy
from dateutil.parser import parse
from datetime import datetime

"""
Handle everything related to SMS
-MV Karan
"""

class SMS(object):
    def __init__(self, exotel):
        self.sid = None
        self.from_num = None
        self.to = None
        self.body = None
        self.priority = 'normal'
        self.status_callback = None
        self.status = None
        self.price = None
        self.date_created = None
        self.date_updated = None
        self.date_sent = None
        self.exotel = exotel

    """
    Validate if all the mandatory parameters for the API are set or not.
    -MV Karan
    """
    def validate(self):
        if(not self.from_num or not self.to or not self.body):
            raise InsufficientSMSDetailsError()

    """
    Set instance attributes from a dict passed as arg
    -MV Karan
    """
    def create(self,sms_info):
        for k,v in sms_info.items():
            if(hasattr(self, k)):
                setattr(self, k, v)
            else:
                raise InvalidSMSDetailsError()
        return

    """
    Send the SMS
    -MV Karan
    """
    def send(self):
        #Validate to check if all the mandatory fields are present or not [MVK]
        self.validate()

        #Prepare all the POST data for the API request [MVK]
        post_data = {
        'From' : self.from_num,
        'To' : self.to,
        'Body' : self.body,
        'Priority' : self.priority
        }

        #Check if optional params are presen and include if so [MVK]
        if(self.status_callback):
            post_data['StatusCallback'] = self.status_callback


        #Form the request to be sent [MVK]
        req = requests.Request \
        (method='POST', auth=(self.exotel.sid, self.exotel.token), \
         url= self.exotel.api_base_url +'/Sms/send.json', \
         data=post_data)

        #Send the request to the throttler [MVK]
        throttledRequest = self.exotel.throttler.submit(req)
        response = throttledRequest.get_response(timeout=None)

        #Check if successful or not. If unsuccessful, return error message [MVK]
        if(response.status_code != 200):
            return response.text

        #Get response data [MVK]
        response_data = json.loads(response.text)
        response_data = response_data['SMSMessage']

        #Create a new SMS object from current and update it to send as response [MVK]
        response_sms = copy.copy(self)
        response_sms.sid = response_data['Sid']
        response_sms.status = response_data['Status']
        response_sms.price = response_data['Price']
        response_sms.date_created = parse(response_data['DateCreated'])
        response_sms.date_updated = parse(response_data['DateUpdated'])

        if(response_data['DateSent']):
            response_sms.date_sent = parse(response_data['DateSent'])
        return response_sms

    """
    Get the dict of all the values in the current object
    -MV Karan
    """
    def details(self):

        data = {}
        data.update((k,v) for k,v in self.__dict__.iteritems() if v is not None)
        del data['exotel'] #Remove the object reference [MVK]
        return data

    """
    Update the current object with updated details of resource
    -MVK
    """
    def update(self):

        #Form the request to be sent [MVK]
        req = requests.Request \
        (method='GET', auth=(self.exotel.sid, self.exotel.token), \
         url= self.exotel.api_base_url +'/Sms/Messages/' + self.sid + '.json', \
         )

        #Send the request to the throttler [MVK]
        throttledRequest = self.exotel.throttler.submit(req)
        response = throttledRequest.get_response(timeout=None)

        #Check if successful or not. If unsuccessful, return error message [MVK]
        if(response.status_code != 200):
            return response.text

        #Get response data [MVK]
        response_data = json.loads(response.text)
        response_data = response_data['SMSMessage']

        #Update the retrieved details in current object [MVK]
        self.status = response_data['Status']
        self.date_updated = parse(response_data['DateUpdated'])
        self.price = response_data['Price']
        return
