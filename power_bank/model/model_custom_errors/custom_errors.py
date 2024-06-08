class NotFoundExceptions(Exception):
    def __init__(self, message="Material doesn't exist"):
        super().__init__(message)
