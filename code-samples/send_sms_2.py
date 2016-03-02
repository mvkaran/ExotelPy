"""
Code sample to send an SMS using Exotel's Python SDK - Alternate Usage
"""

import exotelsdk

exotel = exotelsdk.Exotel()

exotel.sid = 'your_account_sid'
exotel.token = 'your_account_token'

sms = exotel.sms()

sms_info = {
'from_num' : 'your_exophone_number',
'to' : 'receiver_number',
'body' : 'May the force be with you!'
}

sms.create(sms_info)

sms = sms.send()

exotel.bye()
