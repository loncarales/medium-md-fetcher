"""
Custom exception classes
"""


class MediumAPIException(Exception):
    """Base exception for a Medium API client"""

    pass


class AuthenticationError(MediumAPIException):
    """Raised when API authentication fails"""

    pass


class RateLimitExceeded(MediumAPIException):
    """Raised when the API rate limit is exceeded"""

    pass


class ArticleNotFound(MediumAPIException):
    """Raised when the article cannot be found"""

    pass


class InvalidURLError(MediumAPIException):
    """Raised when the provided URL is invalid or cannot be parsed"""

    pass
