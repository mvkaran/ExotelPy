class ExotelSDKError(Exception):
    pass

class AccountUninitializedError(ExotelSDKError):
    pass

class InsufficientSMSDetailsError(ExotelSDKError):
    pass

class InvalidSMSDetailsError(ExotelSDKError):
    pass

class InsufficientCallDetailsError(ExotelSDKError):
    pass

class InvalidCallDetailsError(ExotelSDKError):
    pass
