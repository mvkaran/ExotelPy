"""
Code sample to send an SMS using Exotel's Python SDK
"""

import exotelsdk

exotel = exotelsdk.Exotel()

exotel.sid = 'your_account_sid'
exotel.token = 'your_account_token'

sms = exotel.sms()

sms.from_num = 'your_exophone_number'
sms.to = 'receiver_number'
sms.body = 'May the force be with you!'

sms = sms.send()

exotel.bye()
