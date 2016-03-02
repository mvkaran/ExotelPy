"""
Code sample to connect two numbers using Exotel's Python SDK
"""

import exotelsdk

exotel = exotelsdk.Exotel()

exotel.sid = 'your_account_sid'
exotel.token = 'your_account_token'

call = exotel.call()

call_info = {
'first' : 'first_number_to_dial',
'second' : 'second_number_to_dial',
'caller_id' : 'one_of_your_exophones',
}

call.create(call_info)

call = call.make()

exotel.bye()
