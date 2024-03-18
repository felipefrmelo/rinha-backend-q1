
class UserNotFound(Exception):

    def __init__(self, message: str = 'User not found'):
        self.message = message
        super().__init__(message)


class ValidationError(Exception):

    def __init__(self, message: str = 'Invalid data'):
        self.message = message
        super().__init__(message)
