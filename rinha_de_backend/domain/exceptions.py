

class LimitExceeded(Exception):

    def __init__(self, message: str = 'Limit exceeded'):
        self.message = message
        super().__init__(message)
