class CustomException(Exception):
    """Base class for custom exceptions."""
    def __init__(self, message="A custom exception occurred"):
        self.message = message
        super().__init__(self.message)


class ValidationError(CustomException):
    """Raised when input data fails validation."""
    def __init__(self, field, message="Invalid value"):
        self.field = field
        self.message = f"{field}: {message}"
        super().__init__(self.message)


class AuthenticationError(CustomException):
    """Raised when authentication fails."""
    def __init__(self, user_id=None, message="Authentication failed"):
        self.user_id = user_id
        self.message = f"{message}" + (f" for user {user_id}" if user_id else "")
        super().__init__(self.message)


class ResourceNotFoundError(CustomException):
    """Raised when a requested resource is not found."""
    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(self.message)


class PermissionDeniedError(CustomException):
    """Raised when access is denied due to insufficient permissions."""
    def __init__(self, action, user_role):
        self.action = action
        self.user_role = user_role
        self.message = f"Permission denied: {user_role} cannot perform '{action}'"
        super().__init__(self.message)