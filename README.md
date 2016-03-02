# Exotel Python SDK

Python SDK for Exotel's Call & SMS APIs

- [Installation](#installation)
    - [Using PIP](#using-pip)
    - [Using Easy Install](#using-easy-install)
- [Usage](#usage)
    - [Initialize](#initialize)
    - [Calls](#calls)
        - [Connect Two Numbers](#connect-two-numbers)
        - [Connect Call to Flow or App](#connect-call-to-flow-or-app)
        - [Get Details of a Call](#get-details-of-a-call)
    - [SMS](#sms)
        - [Send an SMS](#send-an-sms)
        - [Get Details of an SMS](#get-details-of-an-sms)
- [Full Code Samples](#full-code-samples)
- [Exceptions](#exceptions)
- [Rate Limits](#rate-limits)
- [More Information](#more-information)
- [Errors](#errors)
- [Contribute](#contribute)
- [License](#license)
- [Change Log](#change-log)

## Installation

The SDK can be installed easily using PIP

### Using PIP

This is the easiest and the recommended method to install the SDK.

```shell
pip install exotelsdk
```

### Using Easy Install

The SDK can be installed even using Easy Install

```shell
easy_install exotelsdk
```

## Usage

### Initialize

Before making any calls / sms, you need to get an instance of your Exotel account

```python
import exotelsdk
exotel = exotelsdk.Exotel() #Create an instance of your account
```

You need to initialize the instance with your `SID` and `Token`. You can get these from the `API` menu under `Settings` in your Exotel account.

```python
exotel.sid = rajnikanth #Example
exotel.token = asd7dfg87dfg8dsugf8s9df7s89f7s89df7df #Example
```
>Note: Not initializing your account instance with the SID and Token will raise a `AccountUninitializedError` exception when trying to make calls / sms.

***
### Close

Once you have finished sending SMS / calls using the `exotel` object, you need to close the connection by calling 

```python
exotel.bye()
```
This is required since the rate-limit throttler has to close. If you forget to call this at the end of your code, your script will not exit!


***
### Calls
***
#### Connect Two Numbers
This is the feature which implements number masking. First, the number in `call.first` is dialled. Once they receive, the number in `call.second` is dialled and connected.

First get an instance of the call object from your `exotel` object.
```python
call = exotel.call()
```
Next, add the details of the call to be dialled.

```python
call.first = '0987654321' #First number to be dialled
call.second = '09988776655' #Second number that will be dialled once the first receives
call.caller_id = '8088919888' #One of your Exophones, which will be shown to both the users
```
Apart from the above mandatory details, you can provide some more additional details like below

```python
call.time_out = 10 #Time (in seconds) to ring both the parties. (Max of 60)
call.time_limit = 300 #Time (in seconds) that the call should last. Call will be cut after this time. (Max. of 14400) (4 hours)
call.status_callback = 'http://example.com/callback' #When the call completes, a HTTP POST request will be made to this URL
```
You can also create a call using a dict as follows

```python
call = exotel.call()

call_info = {
'first' :  '0987654321',
'second' :  '09988776655',
'caller_id' : '8088919888',
'time_out' : 10,
'time_limit' : 300,
'status_callback' : 'http://example.com/callback'
}

call.create(call_info)
```
Make the call using

```python
result = call.make() #Make the call and get the result
```

The `result` will be a string if there is an error, wherein the error message is returned as a string. If the request was successful, the `result` returned will be an object of type `exotel.call`
***

#### Connect Call to Flow or App

With this feature, you can first make an outbound call to a customer and when they receive, connect the call to a Flow or App in your Exotel account.

The usage is similar to the previous one, except that here `call.second` must be the URL of your Flow / App in the form - `http://my.exotel.in/exoml/start/<app-id>` where `<app-id>` is the ID of the App or Flow that you want to connect to.

First get an instance of the call object from your `exotel` object.
```python
call = exotel.call()
```
Next, add the details of the call to be dialled.

```python
call.first = '0987654321' #First number to be dialled
call.second = 'http://my.exotel.in/exoml/start/12345' #URL of the App or Flow that you want to connect to once the customer receives
call.caller_id = '8088919888' #One of your Exophones, which will be shown to both the users
```
Apart from the above mandatory details, you can provide some more additional details like below

```python
call.time_out = 10 #Time (in seconds) to ring both the parties. (Max of 60)
call.time_limit = 300 #Time (in seconds) that the call should last. Call will be cut after this time. (Max. of 14400) (4 hours)
call.status_callback = 'http://example.com/callback' #When the call completes, a HTTP POST request will be made to this URL
```
You can also create a call using a dict as follows

```python
call = exotel.call()

call_info = {
'first' :  '0987654321',
'second' :  'http://my.exotel.in/exoml/start/12345',
'caller_id' : '8088919888',
'time_out' : 10,
'time_limit' : 300,
'status_callback' : 'http://example.com/callback'
}

call.create(call_info)
```
Make the call using

```python
result = call.make() #Make the call and get the result
```

The `result` will be a string if there is an error, wherein the error message is returned as a string. If the request was successful, the `result` returned will be an object of type `exotel.call`
***
#### Get Details of a Call

You can get the details of a call as a dict or by individual details

As a dict:

```python
call.details() #Returns a dict with all the call details as below
```
Individually:

```python
call.sid #Call SID. (Not available until make() is called)
call.first #Number from/to where call was made
call.second #Number where the call was received or the app/flow where call was connected to
call.caller_id #Caller ID that was displayed for the calls
call.time_out #Same as before
call.time_limit #Same as before
call.status #(Not available until make() is called)
call.status_callback #Same as before
call.price #Price of the call (Not available until make() is called)
call.recording_url #URl of the call recording (if available)
call.start_time #Start time of call
call.end_time #End time of call
call.duration #Duration for which the call lasted
call.date_created
call.date_updated
```

To update the details of a call:

```python
call.update()
```

***
### SMS

***

#### Send an SMS

To send a single SMS, first get an instance of the SMS object from your `exotel` object

```python
sms = exotel.sms()
```
Add the details of your SMS to this object. Example values have been show below

```python
sms.from_num = '8088919888' #One of your Exophones
sms.to = '0987654321' 
sms.body = 'Hello from Exotel!' #Don't worry about encoding. ASCII or Unicode will do.
```
Apart from the above mandatory details, you can provide some more additional details like below

```python
sms.priority = 'normal' #For high-priority SMS (like OTP, etc) use 'high'
sms.status_callback = 'http://example.com/callback'
```
>Note: <br/> 1. High-priority SMS will be charged at different rates <br/>    2.  Once the status of the SMS changes to `sent`, `failed` or `failed-dnd`, a HTTP POST request will be made to the given callback URL

You can also create an SMS using a dict as follows

```python
sms = exotel.sms()

sms_info = {
'from_num' : '8088919888',
'to' : '0987654321',
'body' : 'Hello from Exotel!',
'priority' : 'normal',
'status_callback' : 'http://example.com/callback'
}

sms.create(sms_info) #Create an SMS passing a dict as an arg
```
Send the SMS using

```python
result = sms.send() #Send SMS and get the result
```
The `result` will be a string if there is an error, wherein the error message is returned as a string. If the request was successful, the `result` returned will be an object of type `exotel.sms`

***
#### Get Details of an SMS

You can get the details of an SMS as a dict or by individual details

As a dict:

```python
sms.details() #Returns a dict with all SMS details as below
```
Individually:

```python
sms.sid #SMS ID. (Not available until send() is called)
sms.from_num 
sms.to
sms.body 
sms.priority
sms.status_callback
sms.status #Status of the sent SMS. (Not available until send() is called)
sms.price #Price of the sent SMS. (Not available until send() is called)
sms.date_created #Not available until send() is called
sms.date_updated #Not available until send() is called
sms.date_sent #Not available until send() is called
```

To update the details of an SMS:

```python
sms.update()
```
This will update the details of the current sms.

## Full Code Samples

Full code samples to send an SMS and make calls can be viewed at [http://github.com/mvkaran/ExotelPy/tree/master/code-samples](http://github.com/mvkaran/ExotelPy/tree/master/code-samples)

## Exceptions

The SDK raises many exceptions when errors occur. You can catch these exceptions in your application and handle them.

`AccountUnitializedError` This occurs if a exotelsdk.Exotel() object is created and is used to make calls / sms without initializing it with the SID and/or Token.

`InsufficientSMSDetailsError` Occurs if the mandatory fields for an SMS are not provided

`InvalidSMSDetailsError` Occurs if you are trying to create an sms using `sms.create()` by passing an invalid key-value pair in the dict

`InsufficientCallDetailsError` Occurs if the mandatory fields for a Call are not provided

`InvalidCallDetailsError` Occurs if you are trying to create a call using `call.create()` by passing an invalid key-value pair in the dict

## Rate Limits

All Exotel's APIs have a rate limit of 200 requests per minute. Basic throttling of requests are handled by the SDK itself using [RequestsThrottlerExotel](https://pypi.python.org/pypi/RequestsThrottlerExotel). This is limited to only one instace of `exotelsdk.Exotel()` that you create. If you want a global throttler that spans multiple `exotelsdk.Exotel()` instances, we suggest you use some other technique to ensure throttling.

## More Information

For more information regarding terminologies or applets, please check out the official API documentations at `http://support.exotel.in/support/solutions/folders/92360`

## Errors

If you come across any errors / exceptions while using this SDK which is not mentioned here, please create an issue on GitHub or report them to us at `community@exotel.in`

## Contribute

Feel free to contribute to this SDK by forking it. Pull requests are encouraged!
If you would like to contribute to the development of this SDK but are not sure in what way, please get in touch with us on `community@exotel.in`

## License

This SDK is released under The MIT License (MIT)

Copyright (c) 2016 Exotel Techcom Pvt. Ltd. Developed by MV Karan.

## Change Log

`Version 0.1` Initial Release
