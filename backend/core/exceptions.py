class BusinessError(Exception):
    def __init__(self, message, code=1):
        self.message = message
        self.code = code
        super().__init__(message)
