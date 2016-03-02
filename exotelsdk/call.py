from .exception import *
import requests
import base64
import json
import copy
from dateutil.parser import parse
from datetime import datetime

"""
Handle everything related to Calls
-MV Karan
"""

class Call(object):
    def __init__(self, exotel):
        self.sid = None
        self.first = None
        self.second = None
        self.caller_id = None
        self.time_out = None
        self.time_limit = None
        self.status_callback = None
        self.status = None
        self.price = None
        self.recording_url = None
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.date_created = None
        self.date_updated = None
        self.exotel = exotel

    """
    Validate if all the mandatory parameters for the API are set or not.
    -MV Karan
    """
    def validate(self):
        if(not self.first or not self.second or not self.caller_id):
            raise InsufficientCallDetailsError()


    """
    Set instance attributes from a dict passed as arg
    -MV Karan
    """
    def create(self,call_info):
        for k,v in call_info.items():
            if(hasattr(self, k)):
                setattr(self, k, v)
            else:
                raise InvalidCallDetailsError()
        return

    """
    Make the call
    -MV Karan
    """
    def make(self):
        #Validate to check if all the mandatory fields are present or not [MVK]
        self.validate()

        #Prepare all the POST data for the API request [MVK]
        post_data = {
        'From' : self.first,
        'CallerId' : self.caller_id,
        'CallType' : 'trans'
        }

        #Check if trying to connect to agent or a flow and change params accordingly [MVK]
        if(self.second.startswith('http://my.exotel.in/exoml/start/')):
            post_data['Url'] = self.second
        else:
            post_data['To'] = self.second


        #Check if optional params are presen and include if so [MVK]
        if(self.time_limit):
            post_data['TimeLimit'] = self.time_limit
        if(self.time_out):
            post_data['TimeOut'] = self.time_out
        if(self.status_callback):
            post_data['StatusCallback'] = self.status_callback


        #Form the request to be sent [MVK]
        req = requests.Request \
        (method='POST', auth=(self.exotel.sid, self.exotel.token), \
         url= self.exotel.api_base_url +'/Calls/connect.json', \
         data=post_data)

        #Send the request to the throttler [MVK]
        throttledRequest = self.exotel.throttler.submit(req)
        response = throttledRequest.get_response(timeout=None)

        #Check if successful or not. If unsuccessful, return error message [MVK]
        if(response.status_code != 200):
            return response.text

        #Get response data [MVK]
        response_data = json.loads(response.text)
        response_data = response_data['Call']

        #Create a new Call object from current and update it to send as response [MVK]
        response_call = copy.copy(self)
        response_call.sid = response_data['Sid']
        response_call.status = response_data['Status']
        response_call.price = response_data['Price']
        response_call.date_created = parse(response_data['DateCreated'])
        response_call.date_updated = parse(response_data['DateUpdated'])
        response_call.start_time = parse(response_data['StartTime'])
        response_call.end_time = parse(response_data['EndTime']) if response_data['EndTime'] else None
        response_call.duration = response_data['Duration']
        response_call.recording_url = response_data['RecordingUrl'] if response_data['RecordingUrl'] else None

        return response_call

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
         url= self.exotel.api_base_url +'/Calls/' + self.sid + '.json', \
         )

        #Send the request to the throttler [MVK]
        throttledRequest = self.exotel.throttler.submit(req)
        response = throttledRequest.get_response(timeout=None)

        #Check if successful or not. If unsuccessful, return error message [MVK]
        if(response.status_code != 200):
            return response.text

        #Get response data [MVK]
        response_data = json.loads(response.text)
        response_data = response_data['Call']

        #Update the retrieved details in current object [MVK]
        self.status = response_data['Status']
        self.date_updated = parse(response_data['DateUpdated'])
        self.price = response_data['Price']
        self.end_time = parse(response_data['EndTime']) if response_data['EndTime'] else None
        self.duration = response_data['Duration']
        self.recording_url = response_data['RecordingUrl'] if response_data['RecordingUrl'] else None
        return
