
class UserAlreadyExistsException(Exception):
    """Exception raised when a user already exists."""
    def __init__(self, message="User already exists."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"UserAlreadyExistsException: {self.message}"