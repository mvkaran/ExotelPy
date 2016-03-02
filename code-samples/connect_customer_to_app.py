"""
Code sample to connect a customer to your app / flow using Exotel's Python SDK
"""

import exotelsdk

exotel = exotelsdk.Exotel()

exotel.sid = 'your_account_sid'
exotel.token = 'your_account_token'

call = exotel.call()

call_info = {
'first' : 'first_number_to_dial',
'second' : 'http://my.exotel.in/exoml/start/<appid>', #Replace <appid> with your appid
'caller_id' : 'one_of_your_exophones',
}

call.create(call_info)

call = call.make()

exotel.bye()
