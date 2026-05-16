class BaseAppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InvalidStatusTransition(BaseAppException):
    pass

class PaymentRequired(BaseAppException):
    pass

class UserAlreadyExists(BaseAppException):
    pass
